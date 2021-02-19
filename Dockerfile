FROM manimcommunity/manim:v0.3.0

COPY --chown=manimuser:manimuser jupyter_notebooks/pendulum /manim
