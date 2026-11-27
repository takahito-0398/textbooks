"""Draw the mathematical diagrams for the web and printed editions with Pillow."""
from pathlib import Path
from math import atan2, cos, pi, sin
import argparse

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / "assets" / "figures"
INK = "#18282b"
BLUE = "#185672"
TEAL = "#246a59"
RUST = "#923b28"
LIGHT = "#dcebee"
GRID = "#a6b5b7"
WIDTH = 990
FONT = None
font_cache = {}


def canvas(height=480):
    image = Image.new("RGB", (WIDTH, height), "white")
    return image, ImageDraw.Draw(image)


def label(draw, point, text, size=36, fill=INK, anchor="mm"):
    if size not in font_cache:
        font_cache[size] = ImageFont.truetype(FONT, size)
    draw.text(point, text, font=font_cache[size], fill=fill, anchor=anchor)


def line(draw, points, fill=INK, width=5):
    draw.line(points, fill=fill, width=width, joint="curve")


def arrow(draw, start, end, fill=BLUE, size=18, width=5):
    line(draw, [start, end], fill, width)
    x, y = end
    angle = atan2(y - start[1], x - start[0])
    draw.polygon([(x, y)] + [
        (x - size*cos(angle + sign*0.51), y - size*sin(angle + sign*0.51))
        for sign in (-1, 1)
    ], fill=fill)


def circle(draw, x, y, radius, color=BLUE, fill=None, width=5):
    draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=fill, outline=color, width=width)


def loop(draw, x, y, r, start, end, color):
    angles = [start + (end-start)*i/90 for i in range(91)]
    points = [(x+r*cos(a), y-r*sin(a)) for a in angles]
    line(draw, points, color, 7)
    arrow(draw, points[-5], points[-1], color, 24, 7)


def box(draw, bounds, text, fill=LIGHT, size=33):
    draw.rounded_rectangle(bounds, radius=18, fill=fill, outline=GRID, width=2)
    left, top, right, bottom = bounds
    label(draw, ((left+right)/2,(top+bottom)/2), text, size)


def dot(draw, point, color=INK, radius=9):
    circle(draw, *point, radius, color, color, 1)


def save(image, name):
    OUT.mkdir(parents=True, exist_ok=True)
    image.save(OUT / (name + ".png"), optimize=True)


def hemisphere():
    im, d = canvas(470)
    for x,t,detail,sign in [(247,"北の円板","z：反時計回り",1),(743,"南の円板","w：時計回り",-1)]:
        label(d,(x,46),t)
        circle(d,x,255,143,GRID,LIGHT)
        loop(d,x,255,143,0.1,sign*4.9,BLUE if sign>0 else RUST)
        arrow(d,(x,255),(x+100,255),INK)
        label(d,(x,408),detail)
    arrow(d,(420,255),(565,255))
    label(d,(493,212),"g(z)",32)
    save(im,"hemispheres")


def phase_graph():
    im,d=canvas(450)
    arrow(d,(145,355),(870,355),INK)
    arrow(d,(145,405),(145,70),INK)
    label(d,(102,51),"偏角",34)
    label(d,(895,355),"θ",34)
    label(d,(146,391),"0",29)
    label(d,(812,391),"2π",29)
    for y,s in [(120,"2π"),(355,"0")]:
        label(d,(99,y),s,32)
    line(d,[(150,355),(810,355)],TEAL,7)
    line(d,[(150,355),(810,120)],BLUE,7)
    for y,c in [(355,TEAL),(120,BLUE)]:
        dot(d,(810,y),c)
    label(d,(720,115),"g(z) = z",32,BLUE)
    label(d,(630,311),"g(z) = 1",32,TEAL)
    save(im,"phase-lift")


def projection():
    im,d=canvas(425)
    line(d,[(120,355),(830,355)],GRID,3)
    line(d,[(220,390),(220,55)],GRID,3)
    line(d,[(145,398),(772,82)],TEAL,7)
    arrow(d,(220,355),(585,117),BLUE,24,7)
    arrow(d,(220,355),(606,161),TEAL,24,7)
    line(d,[(585,117),(606,161)],RUST,5)
    label(d,(565,78),"u",43,BLUE)
    label(d,(659,170),"Pu",41,TEAL)
    label(d,(798,93),"im P",39,TEAL)
    label(d,(750,374),"赤線は ker P に平行",31)
    save(im,"projection")


def spectrum():
    im,d=canvas(438)
    for i,(x,coordinates,name) in enumerate([
        (182,[(38,-28),(70,49)],"内側"),
        (495,[(38,-28),(105,0)],"境界"),
        (808,[(38,-28),(127,43)],"外側"),
    ]):
        circle(d,x,213,105,GRID,LIGHT)
        line(d,[(x-136,213),(x+146,213)],GRID,2)
        line(d,[(x,79),(x,342)],GRID,2)
        for j,(a,b) in enumerate(coordinates):
            dot(d,(x+a,213-b),TEAL if j==0 else RUST,11)
        label(d,(x,390),name,35)
    save(im,"spectrum")


def skeleton():
    im,d=canvas(385)
    for i,(x,space,cell) in enumerate([(139,"CP⁰","0-cell"),(374,"CP¹","2-cell"),(609,"CP²","4-cell"),(844,"CP³","6-cell")]):
        box(d,(x-95,108,x+95,214),space,size=43)
        label(d,(x,267),cell,33,TEAL)
        if i:
            arrow(d,(x-139,160),(x-98,160))
    label(d,(493,338),"商を取ると S², S⁴, S⁶ が現れる",33)
    save(im,"skeleton")


def koszul():
    im,d=canvas(420)
    coords=[(157,"Λ²V*"),(498,"Λ¹V*"),(841,"Λ⁰V*")]
    for x,t in coords:
        box(d,(x-100,120,x+100,211),t)
    for x in (157,498):
        arrow(d,(x+112,155),(x+229,155))
        arrow(d,(x+229,191),(x+112,191),TEAL)
    label(d,(494,55),"挿入 ι(v)",39,BLUE)
    label(d,(496,275),"外積 s = ℓ ∧",37,TEAL)
    label(d,(496,348),"v ≠ 0 なら ι(v)s + sι(v) = I",35)
    save(im,"koszul")


def orbit():
    im,d=canvas(406)
    for cx,m,name in [(240,1,"S(L)"),(755,2,"S(L²)")]:
        circle(d,cx,215,115,GRID,LIGHT)
        dot(d,(cx+115,215),TEAL,13)
        if m==1:
            dot(d,(cx-115,215),RUST,13)
            label(d,(cx-126,260),"−v",35,RUST)
            label(d,(cx+108,260),"v",35,TEAL)
        else:
            label(d,(cx+95,259),"v ⊗ v",32)
        label(d,(cx,46),name,40)
    arrow(d,(384,214),(600,214),BLUE,23)
    label(d,(494,169),"二乗",36,BLUE)
    save(im,"circle-cover")


def laurent():
    im,d=canvas(476)
    for row,k in enumerate((-3,1)):
        y=132+199*row
        label(d,(100,y),"k = "+str(k),31)
        x=lambda n: 247+(n+5)*79
        line(d,[(x(-5),y),(x(3)+15,y)],GRID,4)
        for n in range(-5,4):
            dot(d,(x(n),y),INK,5)
            label(d,(x(n),y+39),str(n),23)
        arrow(d,(x(0),y-39),(x(3)+22,y-39),BLUE,16,5)
        arrow(d,(x(k),y+87),(x(-5)-12,y+87),TEAL,16,5)
        for n in (range(k+1,0) if k<0 else range(0,k+1)):
            circle(d,x(n),y,17,RUST,None,4)
    save(im,"laurent")


def spectral():
    im,d=canvas(480)
    x=lambda p: 169+113*p
    y=lambda q: 99-77*q
    for q in range(-4,1):
        label(d,(91,y(q)),str(q),32)
        line(d,[(x(0),y(q)),(x(6),y(q))],GRID,2)
        for p in range(7):
            circle(d,x(p),y(q),11,GRID,BLUE if q%2==0 else "white",3)
    for p in range(7):
        label(d,(x(p),433),str(p),32)
    arrow(d,(x(1)+6,y(0)+3),(x(4)-9,y(-2)-7),TEAL,25,8)
    arrow(d,(x(1)+10,y(0)-1),(x(3)-10,y(-1)-7),RUST,20,5)
    label(d,(x(4),118),"d₂",34,RUST)
    label(d,(x(4)+68,y(-2)+22),"d₃",34,TEAL)
    label(d,(84,46),"q",37)
    label(d,(913,430),"p",37)
    save(im,"spectral")


def extension():
    im,d=canvas(392)
    for x,t in [(246,"F² / F⁴ : Z/2"),(743,"F⁴ : Z/2")]:
        box(d,(x-197,71,x+197,166),t,size=41)
    label(d,(494,46),"各層で読む",30)
    label(d,(492,222),"元を全体で持ち上げる",34)
    label(d,(178,316),"μ",48,BLUE)
    label(d,(501,316),"2μ = −μ²",41,BLUE)
    label(d,(848,316),"0",42,INK)
    arrow(d,(239,326),(333,326),TEAL)
    arrow(d,(693,326),(792,326),TEAL)
    label(d,(289,286),"×2",28)
    label(d,(741,286),"×2",28)
    save(im,"extension")


def projective():
    im,d=canvas(434)
    line(d,[(105,359),(906,359)],GRID,4)
    for x,name in [(280,"x"),(716,"y")]:
        dot(d,(x,359),TEAL)
        label(d,(x,399),name,35)
        arrow(d,(x,338),(x,222),TEAL)
        d.ellipse((x-150,65,x+150,210),outline=BLUE,width=5,fill=LIGHT)
        line(d,[(x-90,169),(x+99,113)],RUST,6)
        line(d,[(x-33,185),(x+26,83)],GRID,3)
        label(d,(x,246),"P(E)",32)
    arrow(d,(436,135),(555,135),BLUE)
    label(d,(495,83),"貼る",29)
    save(im,"projective")


def shift():
    im,d=canvas(418)
    for row,y in enumerate((117,296)):
        label(d,(54,y), "入力" if row==0 else "出力",30)
        for i in range(4):
            x=191+193*i
            box(d,(x-51,y-40,x+51,y+40),"e"+str(i),size=36)
    for i in range(3):
        x=191+193*i
        arrow(d,(x+7,164),(x+171,249),BLUE)
    arrow(d,(782,161),(948,244),BLUE)
    label(d,(945,292),"…",32)
    label(d,(191,374),"係数0：余核",35,RUST)
    save(im,"shift")


def fixed_chain():
    im,d=canvas(414)
    for row,(y,exponents,color) in enumerate([(116,(0,1,2),BLUE),(300,(2,1,0),TEAL)]):
        label(d,(97,y),("北域" if row==0 else "南域"),29)
        for i,n in enumerate(exponents):
            x=250+i*235
            box(d,(x-77,y-37,x+77,y+37),("z" if row==0 else "w")+"^"+str(n),size=37)
            if row==0:
                arrow(d,(x,y+45),(x,254),color)
    label(d,(485,380),"z^(-2) 倍し w = 1/z へ",30)
    save(im,"polynomial-charts")


def index_balance():
    im,d=canvas(418)
    for x,t in [(225,"核"),(725,"余核")]:
        label(d,(x,57),t,43)
        for n in range(4 if x==225 else 3):
            box(d,(x-125,112+n*63,x+125,165+n*63),
                ("保存される差" if n==3 else "相殺する成分"),
                LIGHT if n==3 else "#eceeee",28)
    for n in range(3):
        arrow(d,(371,138+n*63),(575,138+n*63),GRID)
    label(d,(497,369),"dim ker − dim coker",36)
    save(im,"index-balance")


def pushforward():
    im,d=canvas(386)
    for x,t in [(160,"T*M"),(495,"法束"),(830,"R^(2N)")]:
        box(d,(x-128,88,x+128,194),t,size=39)
    arrow(d,(292,140),(362,140),BLUE)
    arrow(d,(627,140),(696,140),BLUE)
    for x,t in [(160,"シンボル"),(495,"Thom 類と積"),(830,"延長して Bott")]:
        label(d,(x,249),t,31)
    label(d,(495,329),"台の外では相対類がゼロ",35,TEAL)
    save(im,"pushforward")


def torus_square():
    im,d=canvas(490)
    d.rectangle((326,116,676,391),fill=LIGHT,outline=GRID,width=4)
    for y in (116,391):
        arrow(d,(384,y),(617,y),TEAL,21,7)
    for x in (326,676):
        arrow(d,(x,345),(x,161),BLUE,21,7)
    arrow(d,(668,47),(335,47),RUST,22)
    label(d,(502,81),"右 → 左：g(y) を掛ける",32,RUST)
    label(d,(267,251),"x = 0",33)
    label(d,(738,251),"x = 1",33)
    label(d,(505,441),"上下は同じ係数のまま同一視",32)
    save(im,"torus-gluing")


def cech_subsets():
    im,d=canvas(435)
    vertices=[(495,82),(239,334),(753,334)]
    for i in range(3):
        line(d,[vertices[i],vertices[(i+1)%3]],GRID,6)
    line(d,[vertices[1],vertices[2]],RUST,13)
    for pt in vertices:
        dot(d,pt,BLUE,12)
    for pos,t in [((490,42),"U₂"),((184,352),"U₀"),((806,350),"U₁"),
                  ((496,368),"U₀₁"),((492,234),"U₀₁₂")]:
        label(d,pos,t,39)
    arrow(d,(493,313),(493,260),RUST,20,6)
    label(d,(599,280),"δ = 1",32,RUST)
    save(im,"cech-subsets")


def fixed_weights():
    im,d=canvas(455)
    circle(d,495,221,147,GRID,LIGHT)
    d.ellipse((348,176,642,264),outline=GRID,width=4)
    for y,t,c in [(74,"北：接方向 t",BLUE),(368,"南：接方向 t^(-1)",RUST)]:
        dot(d,(495,y),c,12)
        arrow(d,(509,y),(645,y),c)
        label(d,(784,y),t,36,c)
    label(d,(218,74),"O(k)：1",37,BLUE)
    label(d,(184,368),"O(k)：t^(−k)",37,RUST)
    save(im,"fixed-weights")


def lens_matrix():
    im,d=canvas(458)
    values=[["3","0","0"],["3","3","0"],["1","3","3"]]
    for i,row in enumerate(values):
        for j,v in enumerate(row):
            x,y=125+j*124,159+i*103
            fill={"0":"#f2f4f4","1":"#f5e2db","3":LIGHT}[v]
            box(d,(x-45,y-38,x+45,y+38),v,fill,size=41)
    for i,label_text in enumerate(("u","u²","u³")):
        label(d,(53,159+i*103),label_text,33)
    arrow(d,(449,239),(544,239),BLUE,22)
    for i,t in enumerate(("1","3","9")):
        box(d,(655,119+i*103,826,198+i*103),t,
            "#f5e2db" if i==0 else LIGHT,42)
    label(d,(238,63),"関係行列",37)
    label(d,(740,63),"Smith 標準形",37)
    save(im,"lens-matrix")


def mayer_vietoris():
    im,d=canvas(428)
    d.ellipse((64,53,657,320),fill="#e8f0f2",outline=BLUE,width=5)
    d.ellipse((340,53,929,320),outline=TEAL,width=5)
    label(d,(197,173),"A",53,BLUE)
    label(d,(799,173),"B",53,TEAL)
    label(d,(490,166),"A ∩ B",44)
    arrow(d,(299,196),(390,196),BLUE)
    arrow(d,(692,196),(597,196),TEAL)
    label(d,(497,377),"二つの制限の差を取る",37)
    save(im,"mayer-vietoris")


def diagonal():
    im,d=canvas(446)
    x0,y0=223,385
    arrow(d,(x0,y0),(829,y0),INK)
    arrow(d,(x0,y0),(x0,45),INK)
    line(d,[(x0,y0),(729,63)],TEAL,8)
    label(d,(742,56),"Δ",42,TEAL)
    label(d,(845,415),"第1因子",36)
    label(d,(115,68),"第2因子",36)
    for point in [(386,280),(590,152)]:
        dot(d,point,BLUE)
        arrow(d,(point[0],point[1]+17),(point[0],y0-4),GRID,16,3)
        arrow(d,(point[0]-14,point[1]),(x0+3,point[1]),GRID,16,3)
    save(im,"diagonal")


def grassmann():
    im,d=canvas(437)
    for i,row in enumerate([("a","1","0","0"),("b","0","c","1")]):
        for j,v in enumerate(row):
            x,y=214+j*170,173+i*133
            fill="#d4e9e0" if v=="1" else LIGHT if v!="0" else "#f3f4f4"
            box(d,(x-56,y-44,x+56,y+44),v,fill,44)
    for j in range(4):
        label(d,(214+j*170,73),str(j+1),38,INK)
    label(d,(497,389),"第2列と第4列がピボット",38,TEAL)
    save(im,"grassmann-pivots")


def spectral_flow():
    im,d=canvas(490)
    arrow(d,(134,272),(895,272),INK)
    arrow(d,(168,434),(168,58),INK)
    for r in (-1,0,1):
        line(d,[(190,329-104*r),(835,211-104*r)],TEAL if r==0 else GRID,7)
    dot(d,(503,272),RUST,12)
    label(d,(167,465),"1/2",34)
    label(d,(506,465),"1",34)
    label(d,(835,465),"3/2",34)
    label(d,(531,321),"j = −1 の枝",32,RUST)
    label(d,(911,274),"t",37)
    label(d,(104,68),"固有値",30)
    save(im,"spectral-flow")



def reading_paths():
    im, d = canvas(380)
    rows = [
        (75, '境界の貼り目', '巻き数・曲率', '線束の差', BLUE),
        (190, '円板と円周の対', 'Thom類・完全列', '整数のねじれ', TEAL),
        (305, '微分方程式', '主シンボル・押し出し', '核と余核の差', RUST),
    ]
    for y, start, through, end, color in rows:
        box(d, (20, y-39, 289, y+39), start, size=33)
        box(d, (338, y-39, 654, y+39), through, fill='#f2f5f6', size=31)
        box(d, (706, y-39, 970, y+39), end, size=33)
        arrow(d, (293, y), (333, y), color)
        arrow(d, (659, y), (701, y), color)
    save(im, 'reading-paths')


def degree_coordinates():
    im, d = canvas(345)
    label(d, (495, 43), '同じK類を次数ごとに測る', 36, BLUE)
    entries = [
        (130, '(0次)', '階数'),
        (372, '(2次)', '一次の根の和'),
        (618, '(4次)', '平方の和 ÷ 2'),
        (858, '(6次)', '立方の和 ÷ 6'),
    ]
    for x, degree, name in entries:
        arrow(d, (x, 103), (x, 157), TEAL)
        box(d, (x-113, 166, x+113, 233), degree, size=32)
        label(d, (x, 276), name, 31)
    line(d, [(130, 103), (858, 103)], TEAL, 4)
    save(im, 'degree-coordinates')


def fourier_tracks():
    im, d = canvas(335)
    label(d, (492, 43), '添字を2ずつ戻す', 36, BLUE)
    for y, values, color in [
        (124, (4, 2, 0, -2, -4), BLUE),
        (231, (5, 3, 1, -1, -3), TEAL),
    ]:
        positions = (220, 381, 542, 703, 864)
        label(d, (102, y), '偶数列' if y == 124 else '奇数列', 31, color)
        for x, index in zip(positions, values):
            box(d, (x-45, y-33, x+45, y+33), str(index), size=36)
        for left, right in zip(positions, positions[1:]):
            arrow(d, (left+51, y), (right-51, y), color)
    label(d, (487, 305), '列の中では最初の一つを決めると全て決まる', 31)
    save(im, 'fourier-tracks')


def main():
    global FONT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", default="C:/Windows/Fonts/YuGothM.ttc",
                        help="Path to a Japanese TrueType font")
    FONT = parser.parse_args().font
    for draw in (hemisphere, phase_graph, projection, spectrum, skeleton,
                 koszul, orbit, laurent, spectral, extension, projective,
                 shift, fixed_chain, index_balance, pushforward, torus_square,
                 cech_subsets, fixed_weights, lens_matrix, mayer_vietoris,
                 diagonal, grassmann, spectral_flow, reading_paths,
                 degree_coordinates, fourier_tracks):
        draw()


if __name__ == "__main__":
    main()
