import marimo

__generated_with = "0.23.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Data-driven SVG animations
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Scalable Vector Graphics] (SVG) is a 2D vector graphics language which is a dialect of [XML].
    It can be used inside HTML documents,
    and hence in marimo notebooks using its [Html] class.

    [Scalable Vector Graphics]: https://en.wikipedia.org/wiki/SVG
    [XML]: https://en.wikipedia.org/wiki/XML
    [Html]: https://docs.marimo.io/api/html/#marimo.Html
    """)
    return


@app.cell
def _(mo):
    mo.Html("""
    <svg viewBox="0 0 6 2" xmlns="http://www.w3.org/2000/svg">
      <rect x="1" y="0.5" width="1" height="1" fill="red" fill-opacity="0.5" />
      <circle cx="3" cy="1" r="0.5" fill="green" fill-opacity="0.5" />
      <polygon points="4,1.5 5,1.5 4.5,0.5" fill="blue" fill-opacity="0.5"/>
    </svg>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Since SVG uses a drawing coordinate system (with the $y$ axis pointing downwards), in a mathematical setting
    you probably want to use an initial translation and symmetry transforms to be able to use classic cartesian coordinates (with the $y$ axis pointing upwards) in the rest of the document.

    You then also need to adjust the document view box (the region of the space which is displayed) accordingly to match the desired view box in cartesian coordinates system.
    """)
    return


@app.cell
def _(mo):
    mo.Html("""
    <svg viewBox="0 0 6 2" xmlns="http://www.w3.org/2000/svg">
      <g transform="translate(3, 1)">
        <g transform="scale(1, -1)">
          <!-- square centered on the origin --> 
          <rect x="-0.5" y="-0.5" width="1" height="1" fill="red" fill-opacity="0.5"/>
          <!-- bottom left corner -->
          <polygon points="-3,-1 -2.5,-1, -3,-0.5" fill="black" fill-opacity="0.5" />
        </g>
      </g>
    </svg>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Using Python f-strings, this can be done programmatically:
    """)
    return


@app.cell
def _(mo):
    x_min, x_max, y_min, y_max = -3, 3, -1, 1  # cartesian viewport
    width, height = x_max - x_min, y_max - y_min

    mo.Html(f"""
    <svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
      <g transform="translate({-x_min}, {y_max})">
        <g transform="scale(1, -1)">
          <!-- square centered on the origin --> 
          <rect x="-0.5" y="-0.5" width="1" height="1" fill="red" fill-opacity="0.5"/>
          <!-- bottom left corner -->
          <polygon points="{x_min},{y_min} {x_min + 0.5},{y_min}, {x_min},{y_min + 0.5}" fill="black" fill-opacity="0.5" />
        </g>
      </g>
    </svg>
    """)
    return height, width, x_min, y_max, y_min


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Additional groups (`g` tags) can be inserted to chain geometric transformations.
    """)
    return


@app.cell(hide_code=True)
def _(height, mo, width, x_min, y_max, y_min):
    mo.Html(f"""
    <svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
      <g transform="translate({-x_min}, {y_max})">
        <g transform="scale(1, -1)">
          <g transform="translate(2, 0)">
            <g transform="rotate(45.0)"> 
              <rect x="-0.5" y="-0.5" width="1" height="1" fill="red" fill-opacity="0.5"/>
            </g>
          </g>
          <polygon points="{x_min},{y_min} {x_min + 0.5},{y_min}, {x_min},{y_min + 0.5}" fill="black" fill-opacity="0.5" />
        </g>
      </g>
    </svg>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Using `animateTransform` elements, these transforms can be animated. The `keyTimes` attribute must span the interval $[0, 1]$, but the duration `dur` can slow the animation down.

    For example, with the attributes

    ```
    values="0; 90; 180; 270; 360"
    keyTimes="0; 0.25; 0.5; 0.75; 1.0"
    dur="4s"
    ```

    the animated value will

      - be equal to $0$ when $t=0$, then
      - be equal to $90$ at $t=0.25\times 10=2.5$ sec, then
      - be equal to $180$ at $t=0.5 \times 10 = 5$ sec,
      - etc.
    """)
    return


@app.cell(hide_code=True)
def _(height, mo, width, x_min, y_max, y_min):
    mo.Html(f"""
    <svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
      <g transform="translate({-x_min}, {y_max})">
        <g transform="scale(1, -1)">
          <g transform="translate(2, 0)">
            <g transform="rotate(45.0)">
              <animateTransform
                attributeName="transform"
                type="rotate"
                values="0; 90; 180; 270; 360"
                keyTimes="0; 0.25; 0.5; 0.75; 1.0"
                dur="10s"
                repeatCount="indefinite"
              />
              <rect x="-0.5" y="-0.5" width="1" height="1" fill="red" fill-opacity="0.5"/>
            </g>
          </g>
          <polygon points="{x_min},{y_min} {x_min + 0.5},{y_min}, {x_min},{y_min + 0.5}" fill="black" fill-opacity="0.5" />
        </g>
      </g>
    </svg>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Given what we know at this stage, we can use f-strings again to insert some Python numeric data into the document that will drive the animations.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First let's generate our array of times `t` and the corresponding data array `x`:
    """)
    return


@app.cell
def _(mo, np, plt):
    # Frame rate (frames per seconds)
    FPS = 20.0
    # Period
    T = 10.0

    # Time-dependent data
    dt = 1.0 / FPS
    t = np.arange(0.0, T + dt, dt)


    def x(t):
        return np.sin(2 * np.pi * t / T)


    xt = x(t)

    plt.figure(figsize=(8, 2))  # width=10, height=6 inches
    plt.xlabel("time $t$")
    plt.ylabel("value $x(t)$")
    plt.grid(True)
    mo.center(plt.plot(t, xt))
    return T, t, xt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We format these arrays to make them match what the attributes `keyTimes` and `values` expect:
    """)
    return


@app.cell
def _(T, t, xt):
    key_times = "; ".join(
        str(t_ / T) for t_ in t
    )  # Normalize to fit into the interval [0, 1]
    translations = "; ".join(f"{x},0.0" for x in xt)
    print(f"{key_times = }")
    print(f"{translations = }")
    return key_times, translations


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Then we insert an additional `animateTransform` element to control the translation of our cube:
    """)
    return


@app.cell(hide_code=True)
def _(T, height, key_times, mo, translations, width, x_min, y_max, y_min):
    svg_ = f"""
    <svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
      <g transform="translate({-x_min}, {y_max})">
        <g transform="scale(1, -1)">
          <g transform="translate(2, 0)">
            <animateTransform
              attributeName="transform"
              type="translate"
              values="{translations}"
              keyTimes="{key_times}"
              dur="{T}s"
              repeatCount="indefinite"
            />
            <g transform="rotate(45.0)">
              <animateTransform
                attributeName="transform"
                type="rotate"
                values="0; 90; 180; 270; 360"
                keyTimes="0; 0.25; 0.5; 0.75; 1.0"
                dur="4s"
                repeatCount="indefinite"
              />
              <rect x="-0.5" y="-0.5" width="1" height="1" fill="red" fill-opacity="0.5"/>
            </g>
          </g>
          <polygon points="{x_min},{y_min} {x_min + 0.5},{y_min}, {x_min},{y_min + 0.5}" fill="black" fill-opacity="0.5" />
        </g>
      </g>
    </svg>
    """
    mo.Html(svg_)
    return (svg_,)


@app.cell(hide_code=True)
def _(mo, svg_):
    mo.md(f"""
    Our animation is described as a SVG document. It could be saved as a SVG file and opened in any browser.
    ```svg
    {svg_}
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Helpers
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We have created a `svg` module to build SVG documents in a more "Pythonic" way. Feel free to use it in your own notebook!
    """)
    return


@app.cell
def _():
    from svg import svg

    return (svg,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `svg` factory produces string-like objects (that can be printed and usable with the marimo `Html` class) that represent svg document or fragments.

    1. `svg.XXX` creates an empty element with tag `XXX`.

    2. `svg.XXX(attr1=value1, attr2=value2)` additionally sets attributes for this element.

      - Numeric values are automatically converted to strings: `x=1.0` and `x="1.0"` are equivalent.
      - Substitute underscores to hyphens in attribute names when needed
        (for example, use `fill_opacity=0.5` to set the `fill-opacity` attribute to "0.5").

    3. `svg.XXX(attr1=value1, attr2=value)(svg.YYY, svg.ZZZ)` additionally inserts children into this element.
    """)
    return


@app.cell
def _(mo, svg):
    _svg = svg.svg(viewbox="0 0 6 2", xmlns="http://www.w3.org/2000/svg")(
        svg.rect(x=1.0, y=0.5, width=1.0, height=1.0, fill="red", fill_opacity=0.5),
        svg.circle(cx=3.0, cy=1.0, r=0.5, fill="green", fill_opacity=0.5),
        svg.polygon(points="4,1.5 5,1.5 4.5,0.5", fill="blue", fill_opacity=0.5)
    )
    print(_svg)
    mo.Html(_svg)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Our module also provides a `transform` factory that can be used to translate, rotate, scale, etc. SVG elements;
    refer to the [MDBN doc](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/transform) to see the extent of what's possible.

    A simple example:
    """)
    return


@app.cell(hide_code=True)
def _():
    from svg import transform

    return (transform,)


@app.cell
def _(mo, svg, transform):
    _svg = svg.svg(viewbox="0 0 6 2", xmlns="http://www.w3.org/2000/svg")(
        transform.translate(y=0.5)(
            svg.rect(x=1.0, y=0.5, width=1.0, height=1.0, fill="red", fill_opacity=0.5)
        ),
        transform.scale(y=0.5)(# scaling is always done w.r.t the origin (0, 0) 
                               # translate the SVG shape before and after the scaling to compensate if needed!
            svg.circle(cx=3.0, cy=1.0, r=0.5, fill="green", fill_opacity=0.5)
        ),
        transform.rotate(a=-45.0, x=4.5, y=0.5)(# rotation wrt (4.5, 0.5) of +45 degrees clockwise
            svg.polygon(points="4,1.5 5,1.5 4.5,0.5", fill="blue", fill_opacity=0.5)
        )
    )
    print(_svg)
    mo.Html(_svg)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Finally, we also provide an `animate_transform` factory, that has the same methods as `transform` (`translate`, `rotate`, `scale`, etc.), except that:

    - the arguments to these methods can be a scalar function of a scalar time `t` (a scalar will be interpreted as a constant function),
    - a additional time `T` argument should be given (the animation will be periodic with period `T`).
    """)
    return


@app.cell
def _():
    from svg import animate_transform

    return (animate_transform,)


@app.cell
def _(animate_transform, mo, np, svg):
    _svg = svg.svg(viewbox="0 0 6 2", xmlns="http://www.w3.org/2000/svg")(
        animate_transform.translate(x=lambda t: -1.0 + 1.0 * (t / 6.0), T=6.0)(
            svg.rect(x=1.0, y=0.5, width=1.0, height=1.0, fill="red", fill_opacity=0.5)()
        ),
        animate_transform.scale(y=lambda t: 2.0 * (t / 3.0), T=3.0)( 
            svg.circle(cx=3.0, cy=1.0, r=0.5, fill="green", fill_opacity=0.5)
        ),
        animate_transform.rotate(a=lambda t : 90.0 * np.sin(2 * np.pi * t / 9.0), x=4.5, y=0.5, T=9.0)(
            svg.polygon(points="4,1.5 5,1.5 4.5,0.5", fill="blue", fill_opacity=0.5)
        )
    )
    print(_svg)
    mo.Html(_svg)
    return


if __name__ == "__main__":
    app.run()
