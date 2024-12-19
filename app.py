from flask import Flask, render_template, redirect, request
from names import generate_names, filenames


# Configure application
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """ Render index.html """

    return render_template("index.html", filenames=filenames)


@app.route("/names", methods=["POST"])
def names():
    """ Generate the names according to the user's language choice """

    form = request.form.get("form")
    filename = request.form.get("language")
    language = filenames[filename]
    viewport_width = float(request.form.get("width"))
    viewport_height = float(request.form.get("height"))

    # Generate names
    if form == "generate":
        # Extract data from the generate_names tuple
        pair = generate_names(filename, viewport_width, viewport_height)
        names = pair[0]
        grid_size = pair[1]

        return render_template(
            "names.html", names=names, language=language, filename=filename, filenames=filenames, grid_size=grid_size)

    # Redirect to about.html
    else:
        return redirect("/about")


@app.route("/about")
def about():
    """ Render about.html """

    return render_template("about.html")


if __name__ == "__main__":
    app.run()
