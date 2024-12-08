from flask import Flask, render_template, redirect, request
from languages import generate_names, filenames, GRIDSIZE


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

    # Generate names
    if form == "generate":
        names = generate_names(filename)
        return render_template(
            "names.html", names=names, language=language, filename=filename, filenames=filenames, gridsize=GRIDSIZE)

    # Return to home
    else:
        return redirect("/")


if __name__ == "__main__":
    app.run()
