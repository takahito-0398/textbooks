"""Generate every figure used by elliptic-curves-bsd.md."""

from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
DATA = ROOT / "data" / "experiment.csv"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bsd_experiment import CURVES, count_points, experiment  # noqa: E402

COLORS = {"ink": "#17212b", "blue": "#2364aa", "red": "#c44536", "green": "#2a9d6f", "gold": "#d18b00"}


def setup() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 180, "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})


def curve_branches(a: float, b: float, xmin: float, xmax: float) -> tuple[np.ndarray, np.ndarray]:
    x = np.linspace(xmin, xmax, 2400)
    rhs = x**3 + a * x + b
    y = np.where(rhs >= 0, np.sqrt(np.maximum(rhs, 0)), np.nan)
    return x, y


def save(fig: plt.Figure, name: str) -> None:
    fig.tight_layout()
    fig.savefig(ASSETS / name, bbox_inches="tight")
    plt.close(fig)


def chord_figure() -> None:
    x, y = curve_branches(0, -2, 1.2, 6.3)
    p = np.array([3.0, 5.0])
    q = np.array([1.29, -0.383])
    slope = (q[1] - p[1]) / (q[0] - p[0])
    sum_point = np.array([5.6177, -13.243])
    third = sum_point * np.array([1, -1])
    line_x = np.linspace(1.2, 6.2, 500)
    line_y = p[1] + slope * (line_x - p[0])
    fig, ax = plt.subplots(figsize=(6.4, 5.0))
    ax.plot(x, y, color=COLORS["blue"]); ax.plot(x, -y, color=COLORS["blue"])
    ax.plot(line_x, line_y, color=COLORS["gold"], lw=1.5)
    ax.scatter(*p, color=COLORS["ink"]); ax.scatter(*q, color=COLORS["ink"])
    ax.scatter(*third, color=COLORS["red"]); ax.scatter(*sum_point, color=COLORS["green"])
    ax.vlines(third[0], sum_point[1], third[1], color=COLORS["red"], ls="--")
    for point, label, offset in [(p,"P",(5,4)),(q,"Q",(5,-12)),(third,"R",(5,4)),(sum_point,"P+Q",(5,4))]:
        ax.annotate(label, point, textcoords="offset points", xytext=offset)
    ax.set(xlabel="x", ylabel="y", title=r"Chord construction on $y^2=x^3-2$", xlim=(1.0, 6.4), ylim=(-15.5,15.5))
    save(fig, "01-chord-addition.png")


def tangent_figure() -> None:
    x, y = curve_branches(0, -2, 1.2, 4.6)
    p = np.array([3.0, 5.0]); doubled = np.array([1.29, -0.383]); third = doubled * np.array([1,-1])
    line_x = np.linspace(1.15, 4.5, 400); line_y = 5 + 2.7 * (line_x - 3)
    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    ax.plot(x,y,color=COLORS["blue"]); ax.plot(x,-y,color=COLORS["blue"]); ax.plot(line_x,line_y,color=COLORS["gold"])
    ax.scatter(*p,color=COLORS["ink"]); ax.scatter(*third,color=COLORS["red"]); ax.scatter(*doubled,color=COLORS["green"])
    ax.vlines(third[0], doubled[1], third[1], color=COLORS["red"], ls="--")
    for point,label in [(p,"P"),(third,"R"),(doubled,"2P")]: ax.annotate(label,point,xytext=(5,4),textcoords="offset points")
    ax.set(xlabel="x",ylabel="y",title=r"Tangent construction: $P+P=2P$",ylim=(-3,10))
    save(fig,"02-tangent-doubling.png")


def infinity_figure() -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.8)); ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.plot([0.5,0.5],[0.14,0.84],color=COLORS["gold"],lw=2)
    ax.scatter([0.5,0.5],[0.35,0.65],s=55,color=COLORS["blue"])
    ax.scatter([0.5],[0.9],s=70,color=COLORS["red"],marker="*")
    ax.text(0.53,0.35,"P",va="center"); ax.text(0.53,0.65,"-P",va="center"); ax.text(0.53,0.9,r"$\mathcal{O}$",va="center")
    ax.text(0.5,0.06,r"The vertical line closes at the projective point $\mathcal{O}$",ha="center")
    ax.annotate(r"$P+(-P)=\mathcal{O}$",xy=(0.5,0.88),xytext=(0.63,0.78),arrowprops={"arrowstyle":"->","color":COLORS["red"]})
    save(fig,"03-point-at-infinity.png")


def rank_lattices() -> None:
    fig, axes = plt.subplots(1,2,figsize=(7.2,3.4))
    n=np.arange(-4,5); axes[0].scatter(n,np.zeros_like(n),color=COLORS["blue"]); axes[0].axhline(0,color="#999",lw=.8)
    axes[0].set(title=r"Rank 1: $\mathbb{Z}P$",xlim=(-4.7,4.7),ylim=(-1.2,1.2),yticks=[])
    grid=np.arange(-3,4); xx,yy=np.meshgrid(grid,grid); axes[1].scatter(xx,yy,color=COLORS["green"],s=22)
    axes[1].arrow(0,0,1,0,width=.025,color=COLORS["blue"],length_includes_head=True); axes[1].arrow(0,0,0,1,width=.025,color=COLORS["red"],length_includes_head=True)
    axes[1].set(title=r"Rank 2: $\mathbb{Z}P\oplus\mathbb{Z}Q$",aspect="equal",xlim=(-3.5,3.5),ylim=(-3.5,3.5))
    save(fig,"04-rank-lattices.png")


def finite_field() -> None:
    p=11; curve=CURVES[1]; xs=[]; ys=[]
    for x in range(p):
        for y in range(p):
            if (y*y-x**3-curve.a*x-curve.b)%p==0: xs.append(x); ys.append(y)
    fig,ax=plt.subplots(figsize=(5.2,4.6)); ax.scatter(xs,ys,s=60,color=COLORS["blue"],edgecolor="white")
    ax.set(xticks=range(p),yticks=range(p),xlabel=r"$x\in\mathbf{F}_{11}$",ylabel=r"$y\in\mathbf{F}_{11}$",title=f"Affine points mod 11 ({len(xs)} points)\nplus one point at infinity")
    ax.grid(alpha=.2); save(fig,"05-finite-field-points.png")


def ap_graph() -> None:
    ps=[p for p in range(5,101) if all(p%d for d in range(2,math.isqrt(p)+1))]
    fig,ax=plt.subplots(figsize=(7,4))
    for curve,color in zip(CURVES,[COLORS["blue"],COLORS["red"]]):
        good=[p for p in ps if curve.discriminant%p]; aps=[p+1-count_points(curve,p) for p in good]
        ax.scatter(good,aps,s=26,label=curve.name.split("_")[0],color=color)
    xx=np.linspace(2,100,300); ax.fill_between(xx,-2*np.sqrt(xx),2*np.sqrt(xx),color="#dfe7ee",label=r"Hasse region $|a_p|\leq2\sqrt{p}$")
    ax.axhline(0,color="#777",lw=.8); ax.set(xlabel="prime p",ylabel=r"$a_p=p+1-N_p$",title="Local fluctuations at good primes"); ax.legend()
    save(fig,"06-ap-fluctuations.png")


def product_graph() -> None:
    rows=experiment(5000)
    fig,ax=plt.subplots(figsize=(7,4.4))
    for name,color in [(CURVES[0].name,COLORS["blue"]),(CURVES[1].name,COLORS["red"])]:
        selected=[row for row in rows if row["curve"]==name]
        ax.plot([row["log_log_p"] for row in selected],[row["log_partial_product"] for row in selected],label=name.split("_")[0],color=color,lw=1.4)
    ax.set(xlabel=r"$\log\log X$",ylabel=r"$\log\prod_{p\leq X}N_p/p$",title="Historical BSD partial product (bad primes omitted)"); ax.legend()
    save(fig,"07-bsd-partial-product.png")


def concept_map() -> None:
    labels=[r"$E(\mathbb{Q})$",r"$E(\mathbf{F}_p)$",r"$N_p$",r"$a_p$",r"$L(E,s)$",r"$s=1$",r"rank $r$"]
    fig,ax=plt.subplots(figsize=(8.8,2.5)); ax.axis("off")
    xs=np.linspace(.08,.92,len(labels))
    for i,(x,label) in enumerate(zip(xs,labels)):
        ax.text(x,.55,label,ha="center",va="center",bbox={"boxstyle":"round,pad=.35","fc":"white","ec":COLORS["blue"]})
        if i<len(labels)-1: ax.annotate("",xy=(xs[i+1]-.05,.55),xytext=(x+.05,.55),arrowprops={"arrowstyle":"->","color":COLORS["ink"],"lw":1.4})
    for x,label in [(.08,"global arithmetic"),(.38,"local arithmetic"),(.72,"analysis"),(.92,"global structure")]:
        ax.text(x,.18,label,ha="center",color="#4b5964",fontsize=9)
    save(fig,"08-local-global-map.png")


def write_csv() -> None:
    rows=experiment(2000); DATA.parent.mkdir(parents=True,exist_ok=True)
    with DATA.open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)


def main() -> None:
    setup(); write_csv(); chord_figure(); tangent_figure(); infinity_figure(); rank_lattices(); finite_field(); ap_graph(); product_graph(); concept_map()


if __name__ == "__main__": main()
