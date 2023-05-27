from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user # import entire file, rather than class, to avoid circular imports

# Create Users Controller
@app.route('/create')
def create():
    user_input = session.get('input', '')
    return render_template("create.html", user_input = user_input)

@app.route('/process', methods=['POST'])
def process_create():
    session['input'] = request.form
    if not user.User.validate_user(request.form):
        return redirect('/create')
    user.User.save_user(request.form)
    session.clear()
    return redirect("/")



# Read Users Controller

@app.route('/')
def read():
    all_users = user.User.get_all_users()
    return render_template("read.html", all_users = all_users)

@app.route("/users/<int:user_id>")
def user_page(user_id):
    user_info = user.User.get_one_user(user_id)
    return render_template("user_page.html", user_info = user_info)

# Update Users Controller
@app.route("/users/<int:user_id>/edit")
def user_page_edit(user_id):
    user_info = user.User.get_one_user(user_id)
    return render_template("edit_user_page.html", user_info = user_info)

@app.route('/process/edit', methods=['POST'])
def process_edit():
    user.User.update_user(request.form)
    return redirect(f"/users/{request.form['id']}")

# Delete Users Controller
@app.route('/users/delete/<int:user_id>')
def delete_user(user_id):
    user.User.delete_user(user_id)
    return redirect('/')


# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions 
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal




# How to use path variables:
# @app.route('/<int:id>')
# def index(id):
#     user_info = user.User.get_user_by_id(id)
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.