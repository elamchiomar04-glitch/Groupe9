import numpy as np
import xml.etree.ElementTree as ET

# Register svg as the default namespace
ET.register_namespace("", "http://www.w3.org/2000/svg") 

def indent(xml):
    etree = ET.fromstring(xml)
    ET.indent(etree)
    return ET.tostring(etree, encoding="unicode")

def underscore_to_kebab(text):
    return text.replace("_", "-")

class Delegate:
    def __init__(self, fun, lvl):
        self.fun = fun
        self.lvl = lvl
    def __str__(self):
        if self.lvl == 0:
            return str(self.fun)
        else:
            return str(Delegate(self.fun, self.lvl-1)())
    def __repr__(self):
        if self.lvl == 0:
            return repr(self.fun)
        else:
            return repr(Delegate(self.fun, self.lvl-1)())
    def __call__(self, *args, **kwargs):
        return self.fun(*args, **kwargs)

def delegate(lvl):
    return lambda fun: Delegate(fun, lvl)

class SVG:
    def __getattr__(self, tag):
        @delegate(2)
        def elt_fun(**attributes):
            attribute_string = " ".join(f"{underscore_to_kebab(k)}={str(v)!r}" for k, v in attributes.items())
            @delegate(1)
            def elt(*children):
                children_string = " ".join(str(child) for child in children)
                return indent(f"<{tag} {attribute_string}>{children_string}</{tag}>")                
            return elt
        return elt_fun

svg = SVG()

# SVG reference: <https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/transform>
class Transform:
    @staticmethod
    def _make_group(transform):
        def f(*children):
            return svg.g(transform=transform)(*children)
        return f
    @staticmethod
    def matrix(a=1.0, b=0.0, c=1.0, d=0.0, e=0.0, f=0.0):
        return Transform._make_group(transform=f"matrix({a}, {b}, {c}, {d}, {e}, {f})")
    @staticmethod
    def translate(x=0.0, y=0.0):
        return Transform._make_group(transform=f"translate({x}, {y})")
    @staticmethod
    def scale(x=1.0, y=1.0):
        return Transform._make_group(transform=f"scale({x}, {y})")
    @staticmethod
    def rotate(a=0.0, x=0.0, y=0.0):
        return Transform._make_group(transform=f"rotate({a}, {x}, {y})")
    @staticmethod
    def skewX(a=0.0):
        return Transform._make_group(transform=f"skewX({a})")
    @staticmethod
    def skewY(a=0.0):
        return Transform._make_group(transform=f"skewY({b})")

transform = Transform()

class AnimateTransform:
    @staticmethod
    def _make_group(*args, type, T, fps):
        args = list(args)
        for i, arg in enumerate(args):
            if not callable(arg):
                args[i] = lambda t, arg=arg: arg
        dt =  1.0 / fps
        t = [t_ for t_ in np.arange(0.0, T + dt, dt) if t_ / T <= 1.0]
        key_times = [str(t_ / T) for t_ in t]
        values = [[arg(t_) for arg in args] for t_ in t]
        def f(*children):
            animateTransform = svg.animateTransform(
                attributeName="transform",
                type=type,
                keyTimes="; ".join(key_times),
                values="; ".join(
                    [",".join([str(v) for v in value]) for value in values]
                ),
                dur=f"{T}s",
                repeatCount="indefinite")
            return svg.g()(animateTransform, *children)
        return f
    @staticmethod
    def matrix(a=1.0, b=0.0, c=1.0, d=0.0, e=0.0, f=0.0, T=1.0, fps=30.0):
        return AnimateTransform._make_group(a, b, c, d, e, f, type="matrix", T=T, fps=fps)
    @staticmethod
    def translate(x=0.0, y=0.0, T=1.0, fps=30.0):
        return AnimateTransform._make_group(x, y, type="translate", T=T, fps=fps)
    @staticmethod
    def scale(x=1.0, y=1.0, T=1.0, fps=30.0):
        return AnimateTransform._make_group(x, y, type="scale", T=T, fps=fps)
    @staticmethod
    def rotate(a=0.0, x=0.0, y=0.0, T=1.0, fps=30.0):
        return AnimateTransform._make_group(a, x, y, type="rotate", T=T, fps=fps)
    @staticmethod
    def skewX(a=0.0, T=1.0, fps=30.0):
        return AnimateTransform._make_group(a, type="skewX", T=T, fps=fps)
    @staticmethod
    def skewY(a=0.0, T=1.0, fps=30.0):
        return AnimateTransform._make_group(a, type="skewY", T=T, fps=fps)

animate_transform = AnimateTransform()