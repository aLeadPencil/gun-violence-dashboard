import dash_html_components as html

navbar = html.Header(
    html.Div(
        className="nav-container",
        children = [
            html.Div(
                className="nav",
                children = [
                    html.A(
                        href='/',
                        children=['Home']
                    ),
                    html.A(
                        href='/data-preview',
                        children=['Data Preview']
                    ),
                    html.A(
                        href='/dashboard',
                        children=['Dashboard']
                    ),
                    html.A(
                        href='/contact',
                        children=['Contact']
                    )
                ]
            )
        ]
    ),
)