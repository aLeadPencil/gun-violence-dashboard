import dash_html_components as html

def create_footer_dashboard():
    footer = html.Footer(
        html.Div(
            className = 'contact',
            
            children = html.Ul(
                children = [
                    html.Li(
                        html.A(
                            href = 'https://www.linkedin.com/in/kvn-chu/',
                            target = '_blank',
                            children = ['LinkedIn'],
                        )
                    ),

                    html.Li(
                        html.A(
                            href = 'https://github.com/aLeadPencil',
                            target = '_blank',
                            children = ['GitHub'],
                        )
                    ),

                    html.Li(
                        html.A(
                            href = 'mailto:kchu8150@gmail.com',
                            target = '_blank',
                            children = ['Email Me'],
                        )
                    )
                ]
            )
        )
    )

    return footer

def create_footer_datatable():
    footer = html.Footer(
        html.Div(
            className = 'contact',
            
            children = html.Ul(
                children = [
                    html.Li(
                        html.A(
                            href = 'https://www.linkedin.com/in/kvn-chu/',
                            target = '_blank',
                            children = ['LinkedIn']
                        )
                    ),

                    html.Li(
                        html.A(
                            href = 'https://github.com/aLeadPencil',
                            target = '_blank',
                            children = ['GitHub']
                        )
                    ),

                    html.Li(
                        html.A(
                            href = 'mailto:kchu8150@gmail.com',
                            target = '_blank',
                            children = ['Email Me']
                        )
                    )
                ]
            )
        )
    )

    return footer

if __name__ == '__main__':
    create_footer_dashboard()
    create_footer_datatable()