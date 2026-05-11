import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Redstart: A Lightweight Reusable Booster
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.image(src="public/images/redstart.png")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Project Redstart is an attempt to design the control systems of a reusable booster during landing.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In principle, it is similar to SpaceX's Falcon Heavy Booster.

    >The Falcon Heavy booster is the first stage of SpaceX's powerful Falcon Heavy rocket, which consists of three modified Falcon 9 boosters strapped together. These boosters provide the massive thrust needed to lift heavy payloads—like satellites or spacecraft—into orbit. After launch, the two side boosters separate and land back on Earth for reuse, while the center booster either lands on a droneship or is discarded in high-energy missions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.center(
        mo.Html("""
    <iframe width="560" height="315" src="https://www.youtube.com/embed/RYUr-5PYA7s?si=EXPnjNVnqmJSsIjc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>""")
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Dependencies
    """)
    return


@app.cell
def _():
    import scipy
    import scipy.integrate as sci

    import matplotlib as mpl
    import matplotlib.pyplot as plt

    import numpy as np
    import numpy.linalg as la

    return np, plt, sci


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Model

    The Redstart booster in model as a rigid tube of length $\ell$ and negligible diameter whose mass $M$ is uniformly spread along its length. It may be located in 2D space by the coordinates $(x, y)$ of its center of mass and the angle $\theta$ it makes with respect to the vertical (with the convention that $\theta > 0$ for a left tilt, i.e. the angle is measured counterclockwise)

    This booster has an orientable reactor at its base ; the force that it generates is of amplitude $f \geq 0$ and the angle of the force with respect to the booster axis is $\phi$ (with a counterclockwise convention).

    We assume that the booster is subject to gravity, the reactor force and that the friction of the air is negligible.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.center(mo.image(src="public/images/geometry.svg"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Constants

    For the sake of simplicity (this is merely a toy model!) in the sequel we assume that:

    - the total length $\ell$ of the booster is 2 meters,
    - its mass $M$ is 1 kg,
    - the gravity constant $g$ is 1 m/s^2.

    This set of values is completely unrealistic, but very simple! It will simplify our computations and will not fundamentally impact the structure of the booster dynamics.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Getting Started
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Constants

    Define the Python constants `g`, `M` and `l` that correspond to the gravity constant, the mass and half-length of the booster.
    """)
    return


@app.cell
def _():
    g = 1
    M = 1
    l = 2
    return M, g, l


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Forces

    Compute the cartesian coordinates $f_x$ and $f_y$ of the force applied to the booster by the reactor, functions of $f$, $\theta$ and $\phi$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Pour modéliser les forces appliquées par le réacteur, nous adoptons le repère cartésien suivant :
    - L'axe $x$ représente l'**horizontale** (dirigé vers la droite).
    - L'axe $y$ représente la **verticale** (dirigé vers le haut).

    **Justification de la force de poussée ($f$) :**
    L'intensité $f$ (avec $f \ge 0$) correspond à la norme de la force propulsive. D'après le principe d'action-réaction de Newton, l'éjection des gaz de combustion vers le bas par la tuyère engendre une force de réaction de même intensité appliquée sur la fusée, dirigée vers le haut (le long de l'axe de symétrie du propulseur).

    Dans notre configuration, l'angle 0 correspond à un alignement parfait de la fusée avec l'axe vertical $y$. L'angle total de la force de poussée par rapport à cette verticale est la somme de l'inclinaison du propulseur ($\theta$) et de l'orientation de la tuyère ($\phi$).

    Puisque nos angles sont définis par rapport à la verticale, on utilise la trigonométrie pour décomposer le vecteur de poussée sur nos deux axes :
    - Composante horizontale : $f_x = f \sin(\theta + \phi)$
    - Composante verticale : $f_y = f \cos(\theta + \phi)$
    """)
    return


@app.cell
def _(np):
    def fx(f, theta, phi):
        return f * np.sin(theta + phi)

    def fy(f, theta, phi):
        return f * np.cos(theta + phi)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Center of Mass

    Give the ordinary differential equation that governs the evolution of the position $(x, y)$ of the center of mass of the booster.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Appliquons le Principe Fondamental de la Dynamique (PFD) au centre de masse du propulseur.

    La somme des forces (Poids $\vec{P}$ et Force du réacteur $\vec{F}_R$) est égale à la masse fois l'accélération :
    $$M {\vec{a}} = \vec{P} + \vec{f}$$

    En projetant sur notre repère cartésien (axe $x$ vertical vers le haut, axe $y$ horizontal vers la gauche) :
    - $\vec{P} = -Mg \vec{y}$
    - $\vec{F} = f_x \vec{x} + f_y \vec{y}$

    On obtient le système d'équations différentielles suivant pour la position $(x, y)$ :

    $$M \ddot{y} = f_y - M g \implies \ddot{y} = \frac{f_y}{M} - g$$
    $$M \ddot{x} = f_x \implies \ddot{x} = \frac{f_x}{M}$$
    """)
    return


@app.cell
def _(l, np):
    def x(theta):
        return (l/2 )*np.cos(theta) 
    def y(theta):
        return (l/2)*np.sin(theta)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Moment of inertia

    Compute the [moment of inertia](https://en.wikipedia.org/wiki/Moment_of_inertia) $J$ of the booster and define the corresponding Python variable `J`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Le propulseur est modélisé comme une tige rigide et homogène de masse $M$ et de longueur $\ell$.
    Son moment d'inertie $J$ par rapport à son centre de masse est donné par :
    $$J = \frac{1}{12} M \ell^2$$
    """)
    return


@app.cell
def _(M, l):
    J = (1/12) * M * (l**2)
    return (J,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Tilt

    Give the ordinary differential equation that governs the evolution of the tilt angle $\theta$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Pour étudier la rotation du propulseur autour de son centre de masse $G$, nous utilisons le **Théorème du Moment Cinétique** en projection sur l'axe perpendiculaire au plan $(x, y)$ :
    $$J \ddot{\theta} = \mathcal{M}_G(\vec{P}) + \mathcal{M}_G(\vec{F})$$

    1. **Moment du poids** : Le poids s'applique en $G$, donc   $\mathcal{M}_G(\vec{P}) = 0$.
    2. **Moment de la poussée** : La force s'applique à la base $O$. Dans notre repère $(x,y)$ d'origine $G$, le vecteur position de la base s'écrit :
       $\vec{GO} = -\frac{\ell}{2} \cos(\theta) \vec{x} - \frac{\ell}{2} \sin(\theta) \vec{y}$

       La force de poussée a pour composantes $\vec{F} = f_x \vec{x} + f_y \vec{y}$

       Le calcul du produit vectoriel $\vec{GO} \wedge \vec{F}$ donne le moment de la force par rapport à $G$. Après simplification trigonométrique, on obtient :
       $\mathcal{M}_G(\vec{F}) = - \frac{\ell}{2} f \sin(\phi)$

    L'équation différentielle pour l'angle $\theta$ est donc : $J \ddot{\theta} = - \frac{\ell}{2} f \sin(\phi) \implies \ddot{\theta} = - \frac{f \ell \sin(\phi)}{2 J}$

    L'équation différentielle pour l'angle $\theta$ est donc :
    $$\ddot{\theta} = - \frac{f \ell \sin(\phi)}{2 J}$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Vector Field

    Denote

    - $v_x =\dot{x}$, $v_y = \dot{y}$ the components of the booster center of mass velocity,
    - $\omega = \dot{\theta}$ the angular velocity of the booster.


    What is is dimension $n$ of the state space?
    What is the state $s \in \R^n$ of the booster dynamics?
    Provide the definition of the function $F : \mathbb{R}^{n + 2} \to \mathbb{R}^n$ such that the system evolves
    according to

    $$
    \dot{s} = F(s, f, \phi).
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Pour simuler la dynamique du propulseur, nous devons reformuler notre modèle sous la forme d'un système d'équations différentielles du premier ordre : $\dot{s} = F(s, f, \phi)$.

    Notre système possède 3 degrés de liberté ($x, y, \theta$), chacun associé à sa dérivée temporelle (les vitesses $v_x, v_y, \omega$).
    La dimension de l'espace d'état est donc **$n = 6$**.

    Le vecteur d'état $s \in \mathbb{R}^6$ rassemble les positions et les vitesses :
    $$s = \begin{pmatrix} x \\ v_x \\ y \\ v_y \\ \theta \\ \omega \end{pmatrix}$$

    La fonction $F(s, f, \phi)$ correspond à la dérivée temporelle du vecteur d'état $\dot{s}$. En reprenant les équations issues du PFD et du théorème du moment cinétique, on obtient :

    $$F(s, f, \phi) = \begin{pmatrix} \dot{x} \\ \dot{v}_x \\ \dot{y} \\ \dot{v}_y \\ \dot{\theta} \\ \dot{\omega} \end{pmatrix} = \begin{pmatrix} v_x \\ \frac{f \cos(\theta + \phi)}{M} - g \\ v_y \\ \frac{f \sin(\theta + \phi)}{M} \\ \omega \\ - \frac{f \ell \sin(\phi)}{2 J} \end{pmatrix}$$
    """)
    return


@app.cell
def _(J, M, g, l, np):
    def F(s, f, phi):
        x, vx, y, vy, theta, omega = s
    
        # Vitesses
        dx = vx
        dy = vy
        dtheta = omega
    
        # Accélérations
        dvx = (f * np.sin(theta + phi) / M)
    
        dvy = (f * np.cos(theta + phi) / M) - g
    
        domega = - (f * l * np.sin(phi)) / (2 * J)
    
        return np.array([dx, dvx, dy, dvy, dtheta, domega])

    return (F,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Simulation

    Define a function `redstart_solve` that, given the input parameters:

    - `t_span`: a pair of initial time `t_0` and final time `t_f`,
    - `y0`: the value of `[x, vx, y, vy, theta, omega]` at `t_0`,
    - `f_phi`: a function that given the current time `t` and current state value `y`
         returns the values of the inputs `f` and `phi` in an array.

    returns:

    - `sol`: a function that given a time `t` returns the value of `[x, vx, y, vy, theta, omega]` at time `t` (and that also accepts 1d-arrays of times for multiple state evaluations).

    A typical usage would be:

    ```python
    def free_fall_example():
        t_span = [0.0, 5.0]
        y0 = [0.0, 0.0, 10.0, 0.0, 0.0, 0.0] # [x, vx, y, vy, theta, omega]
        def f_phi(t, y):
            return np.array([0.0, 0.0]) # [f, phi]
        sol = redstart_solve(t_span, y0, f_phi)
        t = np.linspace(t_span[0], t_span[1], 1000)
        y_t = sol(t)[2]
        plt.plot(t, y_t, label=r"$y(t)$ (height in meters)")
        plt.plot(t, l * np.ones_like(t), color="grey", ls="--", label=r"$y=\ell$")
        plt.title("Free Fall")
        plt.xlabel("time $t$")
        plt.grid(True)
        plt.legend()
        return plt.gcf()
    free_fall_example()
    ```
    """)
    return


@app.cell
def _(F, sci):
    def redstart_solve(t_span, y0, f_phi):
        def dynamics(t, s):
            f_val, phi_val = f_phi(t, s)
            return F(s, f_val, phi_val)
    
        res = sci.solve_ivp(
            fun=dynamics,
            t_span=t_span,
            y0=y0,
            dense_output=True,
            max_step=0.05
        )
    
        return res.sol

    return (redstart_solve,)


@app.cell
def _(l, np, plt, redstart_solve):
    def free_fall_example():
        t_span = [0.0, 5.0]
        y0 = [0.0, 0.0, 10.0, 0.0, 0.0, 0.0] # [x, vx, y, vy, theta, omega]
        def f_phi(t, y):
            return np.array([0.0, 0.0]) # [f, phi]
        sol = redstart_solve(t_span, y0, f_phi)
        t = np.linspace(t_span[0], t_span[1], 1000)
        y_t = sol(t)[2]
        plt.plot(t, y_t, label=r"$y(t)$ (height in meters)")
        plt.plot(t, l * np.ones_like(t), color="grey", ls="--", label=r"$y=\ell$")
        plt.title("Free Fall")
        plt.xlabel("time $t$")
        plt.grid(True)
        plt.legend()
        return plt.gcf()
    free_fall_example()

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Freefall test


    In the `free_fall` example scenario. scenario, at what moment should the center of mass of the booster theoretically cross the
    height of $y = \ell$?

    Check your `redstart_solve` function in this scenario and produce a graph that allows us to check the above answer numerically/visually.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    En chute libre ($f=0$), le mouvement vertical est régi par l'équation :
    $$\ddot{y} = -g$$

    En intégrant avec les conditions initiales du scénario ($y(0) = 10$ et $\dot{y}(0) = 0$), on obtient la loi horaire de la position :
    $$y(t) = y(0) - \frac{1}{2} g t^2 = 10 - \frac{1}{2} t^2$$

    Nous cherchons l'instant $t$ tel que $y(t) = \ell = 2$ :
    $$2 = 10 - \frac{1}{2} t^2 \implies \frac{1}{2} t^2 = 8 \implies t^2 = 16$$

    Le centre de masse traverse donc la hauteur $y = \ell$ à **$t = 4$ secondes**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Controlled Landing

    Assume that $x$, $\dot{x}$, $\theta$ and $\dot{\theta}$ are null at $t=0$ and that $y(0)= 10$ and $\dot{y}(0) = - 2$.

    Find a time-varying force $f(t)$ which, when applied in the booster axis ($\theta=0$), yields $y(5)=\ell / 2 = 1$ (the booster is at ground level) and $\dot{y}(5)=0$ (the booster is at rest).

    Simulate the corresponding scenario, display graphically the results and check that your solution works as expected.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Pour réussir l'atterrissage à $t=5$ s avec $y(5)=1$ et $\dot{y}(5)=0$, nous cherchons une commande de poussée linéaire $f(t) = f_0 + f_1 t$.

    En intégrant l'équation différentielle $\ddot{y} = f(t) - 1$ avec les conditions initiales $y(0)=10$ et $\dot{y}(0)=-2$, nous déterminons les coefficients nécessaires :
    - $f_0 = 0.44$
    - $f_1 = 0.384$

    La force appliquée sera donc $f(t) = 0.44 + 0.384 \, t$, avec un angle de tuyère $\phi = 0$.
    """)
    return


@app.cell
def _(np, plt, redstart_solve):
    def controlled_landing_test():
        t_span = [0.0, 5.0]
        # État initial : y=10, vy=-2, le reste est nul
        y0 = [0.0, 0.0, 10.0, -2.0, 0.0, 0.0] 
    
        def f_phi_controlled(t, s):
            # f(t) = 0.44 + 0.384 * t
            f_val = 0.44 + 0.384 * t
            phi_val = 0.0
            return np.array([f_val, phi_val])
        
        sol = redstart_solve(t_span, y0, f_phi_controlled)
        t = np.linspace(t_span[0], t_span[1], 1000)
    
        # Extraction de la hauteur y(t) et de la vitesse vy(t)
        y_t = sol(t)[2]
        vy_t = sol(t)[3]
    
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=True)
    
        # Graphe de la position
        ax1.plot(t, y_t, color="green", label="Hauteur $y(t)$")
        ax1.axhline(1, color="red", ls="--", label="Cible $y=1$")
        ax1.set_ylabel("Hauteur (m)")
        ax1.legend()
        ax1.grid(True)
        ax1.set_title("Atterrissage Contrôlé")
    
        # Graphe de la vitesse
        ax2.plot(t, vy_t, color="orange", label="Vitesse $\dot{y}(t)$")
        ax2.axhline(0, color="black", ls="--")
        ax2.set_ylabel("Vitesse (m/s)")
        ax2.set_xlabel("Temps (s)")
        ax2.legend()
        ax2.grid(True)
    
        return fig

    controlled_landing_test()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Animations

    It's very handy to visualize the evolution of our booster "as a movie"!

    Have a look at the [animations tutorial] to understand the basics of animated SVG documents.

    [animations tutorial]: http://localhost:2718/?file=animations.py
    """)
    return


@app.cell
def _():
    from svg import svg, transform, animate_transform

    return (svg,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Environment

    Create a function `world` whose arguments are:

    - `view_box`: a view box in cartesian coordinates `[x_min, x_max, y_min, y_max]`,

    - `*objects`: (optional) list of extra svg elements (default : `[]`).

    and that returns a SVG string which

    - has the appropriate cartesian view box and frame ($y$-axis upwards),

    - depicts the sky and the ground,

    - depicts a 2 meter wide green ground target centered on $(0, 0)$,

    - displays the objects (if any) inserted on top of the world.

    Test your function with the following scenes:

    ```python
    mo.hstack(
        [
            # Display an empty world
            mo.Html(
                world([-3, 3, -2, 4])
            ),
            # Display a world with a black square on top of the landing pad
            mo.Html(
                world(
                    [-3, 3, -2, 4],
                    svg.rect(x=-1, y=0, width=2, height=2, fill="black"),
                )
            ),
            # Display a world with a red square in the top-left corner of the view box
            # and a blue square on the top-right corner of the view box.
            mo.Html(
                world(
                    [-3, 3, -2, 4],
                    svg.rect(x=-3, y=2, width=2, height=2, fill="red"),
                    svg.rect(x=1, y=2, width=2, height=2, fill="blue"),
                )
            )
        ],
        justify="space-around"
    )
    ```
    """)
    return


@app.function
def world(view_box, *objects):
    x_min, x_max, y_min, y_max = view_box
    width = x_max - x_min
    height = y_max - y_min
    
    objs_str = "\n".join(str(obj) for obj in objects)
    
    svg_content = f"""
    <svg viewBox="{x_min} {-y_max} {width} {height}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <g transform="scale(1, -1)">
            <rect x="{x_min}" y="0" width="{width}" height="{y_max}" fill="#87CEEB" />
            
            <rect x="{x_min}" y="{y_min}" width="{width}" height="{-y_min}" fill="#8B4513" />
            
            <rect x="-1" y="-0.05" width="2" height="0.1" fill="lime" />
            
            {objs_str}
        </g>
    </svg>
    """
    return svg_content


@app.cell
def _(mo, svg):
    mo.hstack(
        [
        
            mo.Html(
                world([-3, 3, -2, 4])
            ),
        
            mo.Html(
                world(
                    [-3, 3, -2, 4],
                    svg.rect(x=-1, y=0, width=2, height=2, fill="black"),
                )
            ),
       
            mo.Html(
                world(
                    [-3, 3, -2, 4],
                    svg.rect(x=-3, y=2, width=2, height=2, fill="red"),
                    svg.rect(x=1, y=2, width=2, height=2, fill="blue"),
                )
            )
        ],
        justify="space-around"
    )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Booster Drawing

    Create a `booster` function that:

    - takes the numeric arguments `x`, `y`, `theta` (in radians), `f` and `phi` (in radians)

    and returns

    - a SVG fragment that represents the body of the booster and the flame of its reactor.
    (The booster drawing can be very simple, for example a rectangle for the body and another one of a different color for the flame will be fine.)

    **Constraint:** make sure that

    - the orientation of the flame is correct,
    - its length is proportional to the force $f$,
    - the flame length is equal to $\ell/2$ when $f=Mg$.


    Test you function in the following scenarios:

    ```python
    mo.hstack(
        [
            mo.Html(
                world(
                    [-3, 3, -2, 4],
                    booster(0, l/2, 0, 0, 0),
                )
            ),
            mo.Html(
                world(
                    [-3, 3, -2, 4],
                    booster(0, l, 0, M * g, 0),
                )
            ),
            mo.Html(
                world(
                    [-3, 3, -2, 4],
                    booster(-l/2, l, np.pi / 4, 2 * M * g, np.pi / 2),
                )
            ),
        ],
        justify="space-around",
    )
    ```
    """)
    return


@app.cell
def _(M, g, l, np):
    def booster(x, y, theta, f, phi):
        # Paramètres de dessin fixes
        w = 0.2          # Épaisseur du corps
        nozzle_w = 0.3   # Largeur de la tuyère à sa base
        nozzle_h = 0.25  # Hauteur de la tuyère
        max_plume_l = 1.0 # Longueur max de la flamme
    

        x_base = x - (l/2) * np.sin(theta)
        y_base = y - (l/2) * np.cos(theta)
        x_top = x + (l/2) * np.sin(theta)
        y_top = y + (l/2) * np.cos(theta)
    

        dir_x = -np.sin(theta + phi)
        dir_y = -np.cos(theta + phi)
    
        perp_x = np.cos(theta + phi)
        perp_y = -np.sin(theta + phi)
    
        tip_x = x_base + nozzle_h * dir_x
        tip_y = y_base + nozzle_h * dir_y
    
    
        c1_x = tip_x + (nozzle_w/2) * perp_x
        c1_y = tip_y + (nozzle_w/2) * perp_y
        c2_x = tip_x - (nozzle_w/2) * perp_x
        c2_y = tip_y - (nozzle_w/2) * perp_y
    
  
        plume_l = min((f / (M * g)) * 0.5, max_plume_l) if M * g > 0 else 0
        p_tip_x = tip_x + plume_l * dir_x
        p_tip_y = tip_y + plume_l * dir_y
    

        pc1_x = tip_x + 0.15 * perp_x
        pc1_y = tip_y + 0.15 * perp_y
        pc2_x = tip_x - 0.15 * perp_x
        pc2_y = tip_y - 0.15 * perp_y


        body = f'<line x1="{x_base}" y1="{y_base}" x2="{x_top}" y2="{y_top}" stroke="black" stroke-width="{w}" stroke-linecap="round" />'
    
        center_of_mass = f'<circle cx="{x}" cy="{y}" r="0.05" fill="white" />'
    
        nozzle_path = f'M {x_base} {y_base} L {c1_x} {c1_y} L {c2_x} {c2_y} Z'
        nozzle = f'<path d="{nozzle_path}" fill="gray" stroke="black" stroke-width="0.02" />'
    
        if f > 0.01:
            plume_path = f'M {pc1_x} {pc1_y} L {p_tip_x} {p_tip_y} L {pc2_x} {pc2_y} Z'
            plume = f'<path d="{plume_path}" fill="orange" opacity="0.8" stroke="none" />'
        else:
            plume = ""
        
        return f"{body}{nozzle}{plume}{center_of_mass}"

    return (booster,)


@app.cell
def _(M, booster, g, l, mo, np):
    mo.hstack(
        [
            mo.Html(
                world(
                    [-3, 3, -2, 4],
                    booster(0, l/2, 0, 0, 0),
                )
            ),
            mo.Html(
                world(
                    [-3, 3, -2, 4],
                    booster(0, l, 0, M * g, 0),
                )
            ),
            mo.Html(
                world(
                    [-3, 3, -2, 4],
                    booster(-l/2, l, np.pi / 4, 2 * M * g, np.pi / 2),
                )
            ),
        ],
        justify="space-around",
    )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Booster Animation

    Create a `booster_anim` function whose arguments are:

    - `x`, `y`, `theta` (in radians), `f` and `phi` (in radians)
    **which are functions of a time `t`**.
    - an animation duration `T`,

    and returns

    - a SVG fragment that represents the animated body of the booster and the flame of its reactor during `T` seconds, then repeats.
    (The booster drawing can be very simple, for example a rectangle for the body and another one of a different color for the flame will be fine.)

    **Constraint:** make sure that

    - the orientation of the flame is correct,
    - its length is proportional to the force $f$,
    - the flame length is equal to $\ell/2$ when $f=Mg$.

    Test your function in the following scenario:

    ```python
    def booster_anim_0():
        T = 5.0
        def x(t):
            return -l/2 + l * (t / T)
        def y(t):
            return l/2 + l/2 * (t / T)
        def theta(t):
            return (t / T) * 2 * np.pi
        def f(t):
            return M * g * (t / T)
        def phi(t):
            return 2 * np.pi * (t / T)
        return booster_anim(x, y, theta, f, phi, T=T)

    mo.Html(
        world([-3, 3, -2, 4], booster_anim_0())
    ).center()
    ```
    """)
    return


@app.cell
def _(M, g, l, np):
    def booster_anim(x_func, y_func, theta_func, f_func, phi_func, T=5.0, N=100):
    
        times = np.linspace(0, T, N)
    
    
        trans_vals = ";".join([f"{x_func(t)},{y_func(t)}" for t in times])
  
        theta_vals = ";".join([f"{np.degrees(theta_func(t))}" for t in times])
        phi_vals = ";".join([f"{np.degrees(phi_func(t))}" for t in times])
    

        d_vals = []
        for t in times:
            f_val = f_func(t)
     
            plume_l = min((f_val / (M * g)) * 0.5, 1.0) if M * g > 0 else 0
            if f_val > 0.01:

                d = f"M 0.15 -0.25 L 0 {-0.25 - plume_l} L -0.15 -0.25 Z"
            else:
                d = "M 0 -0.25 L 0 -0.25 L 0 -0.25 Z"
            d_vals.append(d)
        
        plume_d_vals = ";".join(d_vals)
    
        body = f'<line x1="0" y1="{-l/2}" x2="0" y2="{l/2}" stroke="black" stroke-width="0.2" stroke-linecap="round" />'
        com = '<circle cx="0" cy="0" r="0.05" fill="white" />'
    

        nozzle = '<path d="M 0 0 L 0.15 -0.25 L -0.15 -0.25 Z" fill="gray" stroke="black" stroke-width="0.02" />'
        plume = f'<path fill="orange" opacity="0.8" stroke="none"><animate attributeName="d" values="{plume_d_vals}" dur="{T}s" repeatCount="indefinite"/></path>'
    

        motor_group = f"""
        <g transform="translate(0, {-l/2})">
            <g>
                <animateTransform attributeName="transform" type="rotate" values="{phi_vals}" dur="{T}s" repeatCount="indefinite"/>
                {nozzle}
                {plume}
            </g>
        </g>
        """
    
        svg_content = f"""
        <g>
            <animateTransform attributeName="transform" type="translate" values="{trans_vals}" dur="{T}s" repeatCount="indefinite"/>
            <g>
                <animateTransform attributeName="transform" type="rotate" values="{theta_vals}" dur="{T}s" repeatCount="indefinite"/>
                {body}
                {com}
                {motor_group}
            </g>
        </g>
        """
    
        return svg_content

    return (booster_anim,)


@app.cell
def _(M, booster_anim, g, l, mo, np):
    def booster_anim_0():
        T = 5.0
        def x(t):
            return -l/2 + l * (t / T)
        def y(t):
            return l/2 + l/2 * (t / T)
        def theta(t):
            return (t / T) * 2 * np.pi
        def f(t):
            return M * g * (t / T)
        def phi(t):
            return 2 * np.pi * (t / T)
        return booster_anim(x, y, theta, f, phi, T=T)

    mo.Html(
        world([-3, 3, -2, 4], booster_anim_0())
    ).center()

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Animated Simulation Results

    Let's go back to a booster whose evolution is governed by its system of ordinary differentential equations. Produce a animation of the booster for 5 seconds for each of the following initial value problems:

    1. $(x, \dot{x}, y, \dot{y}, \theta, \dot{\theta}) = (0.0, 0.0, 10.0, 0.0, 0.0, 0.0)$, $f=0$ and $\phi=0$

    2. $(x, \dot{x}, y, \dot{y}, \theta, \dot{\theta}) = (0.0, 0.0, 10.0, 0.0, 0.0, 0.0)$, $f=Mg$ and $\phi=0$

    3. $(x, \dot{x}, y, \dot{y}, \theta, \dot{\theta}) = (0.0, 0.0, 10.0, 0.0, 0.0, 0.0)$, $f=Mg$ and $\phi=\pi/8$

    4. The "controlled landing" scenario (see above).
    """)
    return


@app.cell
def _(booster_anim, mo, np, redstart_solve):
    def physics_landing_anim():
        t_span = [0.0, 5.0]
        y0 = [0.0, 0.0, 10.0, -2.0, 0.0, 0.0] 
    
        def f_phi_controlled(t, s):
            return np.array([0.44 + 0.384 * t, 0.0])
        
        sol = redstart_solve(t_span, y0, f_phi_controlled)

        def x_t(t):
            return sol(t)[0]
        
        def y_t(t):
            return sol(t)[2]
        
        def theta_t(t):
            return sol(t)[4]
        
        def f_t(t):

            return 0.44 + 0.384 * t
        
        def phi_t(t):
            if np.isscalar(t):
                return 0.0
            return np.zeros_like(t)
        

        anim_svg = booster_anim(x_t, y_t, theta_t, f_t, phi_t, T=5.0)
    
    
        return world([-3, 3, -1, 11], anim_svg)

    # On lance l'affichage centré !
    mo.Html(physics_landing_anim()).center()
    return


@app.cell
def _(M, booster_anim, g, mo, np, redstart_solve):
    def physics_deviated_anim():

        t_span = [0.0, 5.0]
        y0 = [0.0, 0.0, 10.0, 0.0, 0.0, 0.0] 
    
        def f_phi_deviated(t, s):
            # f = Mg et phi = pi/8
            return np.array([M * g, np.pi / 8])
        
        sol = redstart_solve(t_span, y0, f_phi_deviated)

        def x_t(t):
            return sol(t)[0]
        
        def y_t(t):
            return sol(t)[2]
        
        def theta_t(t):
            return sol(t)[4]
        
        def f_t(t):

            return M * g
        
        def phi_t(t):
            return np.pi / 8
        
        anim_svg = booster_anim(x_t, y_t, theta_t, f_t, phi_t, T=5.0)
    
        return world([-10, 10, -1, 11], anim_svg)

    mo.Html(physics_deviated_anim()).center()
    return


if __name__ == "__main__":
    app.run()
