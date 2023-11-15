import dash
from dash import html

dash.register_page(__name__,
                   path="/",
                   title="Contexto",
                   name="Contexto")

def layout():
    return html.Div([
        html.H2("Objetivo del proyecto"),
        html.Div([
            html.Div([
                html.P("""Lorem, ipsum dolor sit amet consectetur adipisicing elit. Placeat temporibus porro perferendis consectetur quam eius voluptates eaque voluptas laudantium, animi rem illum neque earum iusto ea tenetur dignissimos reprehenderit quasi?
Officia omnis, beatae magnam nihil laudantium sed, eum fuga laborum ipsum dolorem natus voluptas veritatis atque praesentium. Amet veniam soluta, minima maxime praesentium veritatis asperiores numquam modi sapiente ad molestias!
Enim rerum aperiam explicabo praesentium corrupti quibusdam debitis, mollitia quo ea esse expedita nam quisquam natus, sit ex cumque corporis veniam libero aspernatur voluptatem quas. Quaerat cupiditate qui consectetur porro?
Quisquam quasi, quod sapiente dolorum, alias nihil inventore odio doloribus eaque optio molestias similique obcaecati voluptates, corrupti incidunt totam facere. Quidem deleniti incidunt iusto? At, eveniet impedit! Voluptas, nostrum repellat.""", className="parrafo")
                ], className="col-6"),
            html.Div([
                html.Img(src="assets/tienda.jpg", alt="Ejemplo de una tienda de Liverpool", className="img-fluid")
                ], className="col-6"),
            ], className="row mb-5"),
        html.Div([
            html.Div([
                html.Img(src="assets/renuncias.jpg", alt="Empleado sale con sus pertenencias después de renunciar.", className="img-fluid")
                ], className="col-4"),
            html.Div([
                html.P("""Lorem, ipsum dolor sit amet consectetur adipisicing elit. Placeat temporibus porro perferendis consectetur quam eius voluptates eaque voluptas laudantium, animi rem illum neque earum iusto ea tenetur dignissimos reprehenderit quasi?
Officia omnis, beatae magnam nihil laudantium sed, eum fuga laborum ipsum dolorem natus voluptas veritatis atque praesentium. Amet veniam soluta, minima maxime praesentium veritatis asperiores numquam modi sapiente ad molestias!
Enim rerum aperiam explicabo praesentium corrupti quibusdam debitis, mollitia quo ea esse expedita nam quisquam natus, sit ex cumque corporis veniam libero aspernatur voluptatem quas. Quaerat cupiditate qui consectetur porro?
Quisquam quasi, quod sapiente dolorum, alias nihil inventore odio doloribus eaque optio molestias similique obcaecati voluptates, corrupti incidunt totam facere. Quidem deleniti incidunt iusto? At, eveniet impedit! Voluptas, nostrum repellat.""", className="parrafo")
                ], className="col-8"),
            ], className="row mb-5"),
        ], className="container mt-3")