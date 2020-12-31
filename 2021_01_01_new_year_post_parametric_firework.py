class NewYearPost(MovingCameraScene):
    def construct(self):
        self.camera_frame.move_to(3*UP)
        text = MathTex(
            r" s(t) &=\left( \begin{array}{c} "
            r"x(t)"
            r"\\ y(t)"
            r"\end{array} \right)"
            r"\\ &=\left( \begin{array}{c} "
            r"v_0 t \cos(\theta)"
            r"\\ v_0 t \sin(\theta) - \frac{1}{2}gt^2"
            r"\end{array} \right)"
        )

        text.to_corner(DL).shift(3*UP)
        def func(t):
            v0=10
            theta=0.85*PI/2
            g= 9.81
            return np.array((v0*t*np.cos(theta), v0*t*np.sin(theta)-0.5*g*t**2, 0))

        rocket = ParametricFunction(func, t_max=1, fill_opacity=0).set_color(WHITE)
        dot = Dot().set_color(WHITE)
        dot2 = Dot().set_color(WHITE).move_to(rocket.get_end())
        self.add(dot)
        self.play(Write(rocket),rate_func= linear)
        self.add(dot2)
        all_sparcs= VGroup()
        for theta in np.random.uniform(0, TAU , 90):
            def func2(t):
                v0=10
                g= 9.81
                return np.array((v0*t*np.cos(theta)+dot2.get_x(), v0*t*np.sin(theta)-0.5*g*t**2+dot2.get_y(), 0))
            sparcle = ParametricFunction(func2,t_min=0.04, t_max=0.3, fill_opacity=0).set_color(ORANGE)
            all_sparcs.add((sparcle))
        self.play(*[Write(x) for x in all_sparcs.submobjects], run_time= 0.8, rate_func= linear)
        dots = [Dot(point=[x,y,0]) for x,y in zip(np.random.uniform(-4,4,10),np.random.uniform(0,6,10))]
        self.play(*[Flash(dot) for dot in dots], lag_ratio=0.2)
        dots = [Dot(point=[x,y,0]) for x,y in zip(np.random.uniform(-4,4,10),np.random.uniform(0,6,10))]
        self.play(FadeIn(text),*[Flash(dot) for dot in dots], lag_ratio=0.2)
        dots = [Dot(point=[x,y,0]) for x,y in zip(np.random.uniform(-4,4,30),np.random.uniform(0,6,30))]
        self.play(*[Flash(dot) for dot in dots], lag_ratio=0.2)

        banner = ManimBanner(dark_theme=True).scale(0.3).to_corner(DR)
        self.play(FadeIn(banner.shift(3*UP)))
        self.play(banner.expand())
        self.play(FadeOut(banner))
