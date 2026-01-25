from js import document, setTimeout, setInterval, window, prompt, Date, localStorage
from pyodide import create_once_callable, create_proxy
from random import randint, choice


# flake8: noqa

_valid_colors = [
    "white",
    "silver",
    "gray",
    "black",
    "red",
    "maroon",
    "yellow",
    "olive",
    "lime",
    "green",
    "aqua",
    "teal",
    "blue",
    "navy",
    "fuchsia",
    "purple",
    "orange",
    "mediumvioletred",
    "deeppink",
    "palevioletred",
    "hotpink",
    "lightpink",
    "pink",
    "darkred",
    "firebrick",
    "crimson",
    "indianred",
    "lightcoral",
    "salmon",
    "darksalmon",
    "lightsalmon",
    "orangered",
    "tomato",
    "darkorange",
    "coral",
    "darkkhaki",
    "gold",
    "khaki",
    "peachpuff",
    "palegoldenrod",
    "moccasin",
    "papayawhip",
    "lightgoldenrodyellow",
    "lemonchiffon",
    "lightyellow",
    "brown",
    "saddlebrown",
    "sienna",
    "chocolate",
    "darkgoldenrod",
    "peru",
    "rosybrown",
    "goldenrod",
    "sandybrown",
    "tan",
    "burlywood",
    "wheat",
    "navajowhite",
    "bisque",
    "blanchedalmond",
    "cornsilk",
    "darkgreen",
    "darkolivegreen",
    "forestgreen",
    "seagreen",
    "olivedrab",
    "mediumseagreen",
    "limegreen",
    "springgreen",
    "mediumspringgreen",
    "darkseagreen",
    "mediumaquamarine",
    "yellowgreen",
    "lawngreen",
    "chartreuse",
    "lightgreen",
    "greenyellow",
    "palegreen",
    "darkcyan",
    "lightseagreen",
    "cadetblue",
    "darkturquoise",
    "mediumturquoise",
    "turquoise",
    "cyan",
    "aquamarine",
    "paleturquoise",
    "lightcyan",
    "darkblue",
    "mediumblue",
    "midnightblue",
    "royalblue",
    "steelblue",
    "dodgerblue",
    "deepskyblue",
    "cornflowerblue",
    "skyblue",
    "lightskyblue",
    "lightsteelblue",
    "lightblue",
    "powderblue",
    "indigo",
    "darkmagenta",
    "darkviolet",
    "darkslateblue",
    "blueviolet",
    "darkorchid",
    "magenta",
    "slateblue",
    "mediumslateblue",
    "mediumorchid",
    "mediumpurple",
    "orchid",
    "violet",
    "plum",
    "thistle",
    "lavender",
    "mistyrose",
    "antiquewhite",
    "linen",
    "beige",
    "whitesmoke",
    "lavenderblush",
    "oldlace",
    "aliceblue",
    "seashell",
    "ghostwhite",
    "honeydew",
    "floralwhite",
    "azure",
    "mintcream",
    "snow",
    "ivory",
    "darkslategray",
    "dimgray",
    "slategray",
    "lightslategray",
    "darkgray",
    "lightgray",
    "gainsboro",
]


def _is_valid_element(func_name):
    """
    Allows us to throw a helpful error message if someone passes a raw value
    to a function that accepts a DOM element. For some reason, Transcrypt
    wants this definition before it's used, so it has to be at the top of the
    file.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            element = args[0]
            if isinstance(element, (float, int, str)):
                raise Exception(
                    f"""
Error in {func_name}(), invalid element passed as first argument
    - '{element}' is not a valid element!
    - Did you pass an element created with add_image(), add_text(), or add_button() as the first argument?
"""
                )
            # This will catch functions passed in where an element is exepected
            # or `undefined` JS vars that sneak through.
            elif callable(element) or not element:
                raise Exception(
                    f"""
Error in {func_name}(), invalid element passed as first argument\n"
    - Did you pass an element created with add_image(), add_text(), or add_button() as the first argument?
"""
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator


def add_audio(filename):
    """
    Adds an audio file.

    Parameters:
        - filename (str): The filename.

    Returns:
        - The audio element.

    Example usage:
        audio_element = add_audio("never-gonna-give-you-up.mp3")
    """

    element = document.createElement("audio")
    callback_function = create_once_callable(
        lambda _: _filename_not_found(filename, "add_audio")
    )

    element.addEventListener("error", callback_function)
    element.src = filename

    document.body.appendChild(element)

    return element


def add_background(filename):
    """
    Adds a background image.

    Parameters:
        - filename (str): The filename.

    Example usage:
        add_background("flying-cats.png")
    """

    element = document.createElement("img")
    callback_function = create_once_callable(
        lambda _: _filename_not_found(filename, "add_background")
    )

    element.addEventListener("error", callback_function)
    element.src = filename

    canvas = document.getElementById("canvas")

    if canvas:
        canvas.style.backgroundImage = f"url({filename})"
    else:
        document.querySelector("html").style.backgroundImage = f"url({filename})"


def add_background_audio(filename):
    """
    Adds background audio which plays when you click the "Start" button.

    Parameters:
        - filename (str): The filename.

    Example usage:
        add_background_audio("never-gonna-give-you-up.mp3")
    """

    element = document.createElement("audio")
    callback_function = create_once_callable(
        lambda _: _filename_not_found(filename, "add_background_audio")
    )
    element.addEventListener("error", callback_function)

    element.src = filename
    element.id = "bg-music"
    element.loop = True

    document.body.appendChild(element)


def add_button(text):
    """
    Adds a button.

    Parameters:
        - text (str): The text on the button.

    Returns:
        - The button element.

    Example usage:
        button = add_button("Click Me")
    """

    element = document.createElement("button")
    element.textContent = text
    element.style.alignSelf = "flex-start"

    canvas = document.getElementById("canvas")

    if canvas:
        canvas.appendChild(element)
    else:
        document.body.appendChild(element)

    return element


def add_image(filename, size=None):
    """
    Adds an image to the page.

    Parameters:
        - filename (str): The filename.
        - size (int): The size, in pixels (optional).

    Returns:
        - The image element.

    Example usage:
        taco_image = add_image("taco.png")
    """

    element = document.createElement("img")
    callback_function = create_once_callable(
        lambda _: _filename_not_found(filename, "add_image")
    )
    element.addEventListener("error", callback_function)
    element.src = filename

    if size:
        element.style.width = str(size) + "px"

    canvas = document.getElementById("canvas")

    if canvas:
        canvas.appendChild(element)
    else:
        document.body.appendChild(element)

    return element


def add_text(text, size=18):
    """
    Adds text to the page.

    Parameters:
        - text (str): The text to add to the page.
        - size (int): The size, in pixels (optional).

    Returns:
        - The text element.

    Example usage:
        mylibrary_text = add_text("mylibrary is cool!")
    """

    element = document.createElement("p")
    text = str(text)
    element.innerHTML = text.replace("\\n", "<br />")
    element.innerHTML = text.replace("\n", "<br />")
    element.style.fontSize = str(size) + "px"
    

    canvas = document.getElementById("canvas")

    if canvas:
        canvas.appendChild(element)
    else:
        document.body.appendChild(element)

    return element


def add_text_input(placeholder):
    """
    Adds a text input to the page.

    Parameters:
        - placeholder (str): The text to display in the input box.

    Returns:
        - The text input element.

    Example usage:
        text_input = add_text_input("Enter your password:")
    """

    element = document.createElement("input")
    element.placeholder = placeholder

    canvas = document.getElementById("canvas")

    if canvas:
        canvas.appendChild(element)
    else:
        document.body.appendChild(element)

    return element


@_is_valid_element("animate_down")
def animate_down(element, distance, time=8, loop=False):
    """
    Animates the element down by the given distance. Can optionally change
    the amount of time the animation takes and whether the element animates
    down and up repeatedly.

    Parameters:
        - element (element): An element to animate.
        - distance (int): The distance the element should travel (in pixels).
        - time (int): The amount of seconds the animation should take (optional).
        - loop (bool): Whether to repeatedly animate down and up.

    Example usage:
        taco_image = add_image("taco.jpg")
        animate_down(taco_image, 100)
    """

    element.style.transition = f"{time}s linear transform"
    start_button = document.getElementById("start")

    element.distance = distance
    element.time = time
    element.animation_direction = "down"

    if element.style.top:
        element.start_position = int(element.style.top[:-2])
    else:
        element.start_position = 0

    callback_function = create_once_callable(lambda _: _translate_y(element, distance))
    
    # If start button is pressed
    if start_button:
        # Add event listener 
        start_button.addEventListener("click", callback_function)
        # If the start button is disabled, then just translate the element right away
        if start_button.disabled:
            _translate_y(element, distance)
    # If there's no start button, translate the element once the page loads
    else:
        _translate_y(element, distance)
    
    if loop:
        element.animation_direction = "up"
        callback_function_proxy = create_proxy(
            lambda _: _loop_animation(element, distance)
        )
        element.addEventListener("transitionend", callback_function_proxy)


@_is_valid_element("animate_left")
def animate_left(element, distance, time=8, loop=False):
    """
    Animates the element left by the given distance. Can optionally change
    the amount of time the animation takes and whether the element animates
    left and right repeatedly.

    Parameters:
        - element (element): An element to animate.
        - distance (int): The distance the element should travel (in pixels).
        - time (int): The amount of seconds the animation should take (optional).
        - loop (bool): Whether to repeatedly animate left and right.

    Example usage:
        taco_image = add_image("taco.jpg")
        animate_left(taco_image, 100)
    """

    element.style.transition = f"{time}s linear transform"
    start_button = document.getElementById("start")

    element.distance = distance
    element.time = time
    element.animation_direction = "left"

    if element.style.left:
        element.start_position = int(element.style.left[:-2])
    else:
        element.start_position = 0

    callback_function = create_once_callable(lambda _: _translate_x(element, -distance))

    # If start button is pressed
    if start_button:
        # Add event listener 
        start_button.addEventListener("click", callback_function)
        # If the start button is disabled, then just translate the element right away
        if start_button.disabled:
            _translate_x(element, -distance)
    # If there's no start button, translate the element once the page loads
    else:
        _translate_x(element, -distance)

    if loop:
        callback_function_proxy = create_proxy(
            lambda _: _loop_animation(element, distance)
        )
        element.addEventListener("transitionend", callback_function_proxy)


@_is_valid_element("animate_right")
def animate_right(element, distance, time=8, loop=False):
    """
    Animates the element right by the given distance. Can optionally change
    the amount of time the animation takes and whether the element animates
    right and left repeatedly.

    Parameters:
        - element (element): An element to animate.
        - distance (int): The distance the element should travel (in pixels).
        - time (int): The amount of seconds the animation should take (optional).
        - loop (bool): Whether to repeatedly animate right and left.

    Example usage:
        taco_image = add_image("taco.jpg")
        animate_right(taco_image, 100)
    """

    element.style.transition = f"{time}s linear transform"
    start_button = document.getElementById("start")
    callback_function = create_once_callable(lambda _: _translate_x(element, distance))

    element.distance = distance
    element.time = time
    element.animation_direction = "right"

    if element.style.left:
        element.start_position = int(element.style.left[:-2])
    else:
        element.start_position = 0
    
    # If start button is pressed
    if start_button:
        # Add event listener 
        start_button.addEventListener("click", callback_function)
        # If the start button is disabled, then just translate the element right away
        if start_button.disabled:
            _translate_x(element, distance)
    # If there's no start button, translate the element once the page loads
    else:
        _translate_x(element, distance)

    if loop:
        callback_function_proxy = create_proxy(
            lambda _: _loop_animation(element, distance)
        )
        element.addEventListener("transitionend", callback_function_proxy)


@_is_valid_element("animate_up")
def animate_up(element, distance, time=8, loop=False):
    """
    Animates the element up by the given distance. Can optionally change
    the amount of time the animation takes and whether the element animates
    up and down repeatedly.

    Parameters:
        - element (element): An element to animate.
        - distance (int): The distance the element should travel (in pixels).
        - time (int): The amount of seconds the animation should take (optional).
        - loop (bool): Whether to repeatedly animate up and down.

    Example usage:
        taco_image = add_image("taco.jpg")
        animate_up(taco_image, 100)
    """

    element.style.transition = f"{time}s linear transform"
    start_button = document.getElementById("start")
    callback_function = create_once_callable(lambda _: _translate_y(element, -distance))

    element.distance = distance
    element.time = time
    element.animation_direction = "up"

    if element.style.top:
        element.start_position = int(element.style.top[:-2])
    else:
        element.start_position = 0

    # If start button is pressed
    if start_button:
        # Add event listener 
        start_button.addEventListener("click", callback_function)
        # If the start button is disabled, then just translate the element right away
        if start_button.disabled:
            _translate_y(element, -distance)
    # If there's no start button, translate the element once the page loads
    else:
        _translate_y(element, -distance)

    if loop:
        element.animation_direction = "up"
        callback_function_proxy = create_proxy(
            lambda _: _loop_animation(element, -distance)
        )
        element.addEventListener("transitionend", callback_function_proxy)


def check_collision(element1, element2, function_to_run):
    """
    If element1 and element2 collide, function_to_run is called.

    Parameters:
        - element1 (element): An element to check for collisions with.
        - element2 (element): An element to check for collisions with.
        - function_to_run (function): The function to run if element1 hits element2.

    Example usage:
        def cat_caught_taco():
            clear()
            text = add_text("The kitty caught the taco!")
            position_element(text, "center", "center")


        taco_image = add_image("taco.jpg", 100)
        cat_image = add_image("flying-cats.jpg", 100)

        check_collision(taco_image, cat_image, cat_caught_taco)
    """

    def turn_into_proxy(*args):
        _collision(element1, element2, function_to_run)

    callback_function_proxy = create_proxy(turn_into_proxy)

    start_button = document.getElementById("start")
    
    # If start button is pressed
    if start_button:
        # Add event listener 
        start_button.addEventListener(
            "click", create_proxy(lambda _: setInterval(callback_function_proxy, 50))
        )
        # If the start button is disabled, then just set the interval right away
        if start_button.disabled:
            setInterval(callback_function_proxy, 50)
    # If there's no start button, set the interval right away
    else:
        setInterval(callback_function_proxy, 50)


def clear():
    """
    Clear the page of all elements.

    Example usage:
        def clear_page():
            clear()
            after_clear_text = add_text("Page was cleared", 32)
            position_element(after_clear_text, "center", "center")


        before_clear_text = add_text("This is on the page before clearing", 32)
        position_element(before_clear_text, "center", "center")

        clear_page_button = add_button("Clear Page")
        position_element(clear_page_button, "center", 400)

        click(clear_page_button, clear_page)
    """

    image_elements = document.querySelectorAll("#canvas img")
    text_elements = document.querySelectorAll("#canvas p")
    button_elements = document.querySelectorAll("#canvas button:not(#start)")
    input_elements = document.querySelectorAll("input")

    [el.remove() for el in image_elements]
    [el.remove() for el in text_elements]
    [el.remove() for el in button_elements]
    [el.remove() for el in input_elements]


@_is_valid_element("click")
def click(element, function_to_run):
    """
    Call `function_to_run` when `element` is clicked.

    Parameters:
        - element (element): The element to click.
        - function_to_run (function): The function to run if `element` is clicked.

    Example usage:
        def show_text():
            text = add_text("Button was clicked!", 32)
            position_element(text, "center", "center")


        button = add_button("Click Me")
        position_element(button, "center", 400)

        click(button, show_text)
    """

    if not callable(function_to_run):
        raise Exception(
            """
Error in click()
    - The second argument is not a function!
"""
        )

    def click_handler(event):
        # Note that this will use __code__.co_argcount for TAM
        if function_to_run.__code__.co_argcount:
            function_to_run(event.target)
        else:
            function_to_run()

    # allows us to remove the click_handler in vanish() to prevent spam clicks
    element.click_handler = click_handler
    element.addEventListener("click", create_proxy(click_handler))


def _collision(a, b, cb):
    a = a.getBoundingClientRect()
    b = b.getBoundingClientRect()
    if (
        b.x < a.x + a.width
        and b.x + b.width > a.x
        and b.top < a.top + a.height
        and b.top + b.height > a.top
    ):
        cb()


@_is_valid_element("fade_in")
def fade_in(element):
    """
    Fades the `element` from invisible to visible.

    Parameters:
        - element (element): The element to fade in.

    Example usage:
        def fade_text_in():
            fade_in(hidden_text)


        hidden_text = add_text("Hidden Text", 32)
        position_element(hidden_text, "center", 400)
        fade_out(hidden_text)

        fade_in_button = add_button("Fade In")
        position_element(fade_in_button, "center", "center")
        click(fade_in_button, fade_text_in)
    """

    if element.style.transition and "opacity 1s linear" not in element.style.transition:
        element.style.transition += ", opacity 1s linear"
    else:
        element.style.transition = "opacity 1s linear"

    element.classList.remove("fade-out")
    element.classList.add("fade-in")


@_is_valid_element("fade_out")
def fade_out(element):
    """
    Fades the `element` from visible to invisible.

    Parameters:
        - element (element): The element to fade out.

    Example usage:
        def fade_text_out():
            fade_out(text_to_hide)


        text_to_hide = add_text("Text To Hide", 32)
        position_element(text_to_hide, "center", 400)

        fade_out_button = add_button("Fade Out")
        position_element(fade_out_button, "center", "center")
        click(fade_out_button, fade_text_out)
    """

    if element.style.transition and "opacity 1s linear" not in element.style.transition:
        element.style.transition += ", opacity 1s linear"
    else:
        element.style.transition = "opacity 1s linear"

    element.classList.remove("fade-in")
    element.classList.add("fade-out")


def _filename_not_found(filename, function_name):
    raise Exception(
        f"""
Error in {function_name}()
    - '{filename}' is not a valid filename!
"""
    )


@_is_valid_element("get_input_value")
def get_input_value(element):
    """
    Gets the value of the input `element`.

    Parameters:
        - element (element): The element to get the value from.

    Example usage:
        def login():
            password = get_input_value(password_input)
            clear()
            if password == "secretpassword":
                logged_in_text = add_text("You've logged in!", 32)
                position_element(logged_in_text, "center", 400)


        password_input = add_text_input("Enter your password")
        position_element(password_input, "center", 400)

        login_button = add_button("Login")
        position_element(login_button, "center", "center")
        click(login_button, login)
    """

    return element.value


@_is_valid_element("_loop_animation")
def _loop_animation(element, distance):
    if element.animation_direction == "left":
        element.animation_direction = "right"
        _translate_x(element, distance)
    elif element.animation_direction == "right":
        element.animation_direction = "left"
        _translate_x(element, -distance)
    elif element.animation_direction == "up":
        element.animation_direction = "down"
        _translate_y(element, -distance)
    elif element.animation_direction == "down":
        element.animation_direction = "up"
        _translate_y(element, distance)


def _is_invalid_color(color):
    if color.lower() not in _valid_colors:
        if not color:
            return True
        if color[0] != "#":
            return True
        if len(color) != 7:
            return True
    return False


def _is_invalid_x_position_keyword(x_position):
    return x_position not in ["left", "right", "center"]


def _is_invalid_y_position_keyword(y_position):
    return y_position not in ["top", "bottom", "center"]


def input(s):
    return prompt(s)


def keydown(function_to_run, fast=False):
    """
    Wrapper for more specific keydown functions.
    Passes `function_to_run` to `_keydown` or `_keydown_fast` based on the boolean flag `fast` parameter.
    """
    if not callable(function_to_run):
        raise Exception(
            """
Error in keydown()
    - The first argument is not a function!
"""
        )
    if type(fast) != bool:
        raise Exception(
            """
Error in keydown()
    - The second argument is not a boolean!
"""
        )
    if fast:
        _keydown_fast(function_to_run)
    else:
        _keydown(function_to_run)


def _keydown(function_to_run):
    """
    Runs `function_to_run` when a key is pressed using a standard `keydown` event listenter. The key that is pressed will
    be passed as the first argument to `function_to_run` and will always be
    lowercase.

    Parameters:
        - function_to_run (function): The function to run when a key is pressed.

    Example usage:
        def key_logger(pressed_key):
            update_text(last_key_pressed_text, f"Last key pressed: {pressed_key}")


        last_key_pressed_text = add_text("Last key pressed: ", 32)
        position_element(last_key_pressed_text, "center", 400)

        keydown(key_logger)
    """

    def keydown_listener(event):
        start_button = document.getElementById("start")
        if start_button.disabled == False:
            print()
        else: 
            function_to_run(event.key.lower())
    
    document.body.addEventListener("keydown", create_proxy(keydown_listener))


def _keydown_fast(function_to_run):
    """
    Called by keydown when the second argument is `True`.
    Runs `function_to_run` when a key is pressed using a standard `keydown` event listener. The key that is pressed will
    be passed as the first argument to `function_to_run` and will always be
    lowercase.

    Parameters:
        - function_to_run (function): The function to run when a key is pressed.

    Example usage:
        def move(key):
           if key == "d":
               move_right(wizard, 5)


        wizard = add_image("wizard.png", 100)
        keydown(move, True)
    """
    if hasattr(_keydown_fast, "_keydown_ticking"):
        return

    _keydown_fast._keys_down = {}
    _keydown_fast._keydown_ticking = True
    tickrate = 40

    def keydown_listener(event):
        _keydown_fast._keys_down[event.key] = True

    def keyup_listener(event):
        if event.key in _keydown_fast._keys_down:
            del _keydown_fast._keys_down[event.key]

    def tick():
        for key in _keydown_fast._keys_down:
            function_to_run(key.lower())

    setInterval(create_proxy(tick), tickrate)
    document.body.addEventListener("keydown", create_proxy(keydown_listener))
    document.body.addEventListener("keyup", create_proxy(keyup_listener))


@_is_valid_element("move_down")
def move_down(element, distance):
    """
    Moves the `element` down by the given `distance`.

    Parameters:
        - element (element): The element to move down.
        - distance (int): The distance the `element` should travel (in pixels).

    Example usage:
        def move_taco(pressed_key):
            if pressed_key == "w":
                move_up(taco_image, 10)
            elif pressed_key == "a":
                move_left(taco_image, 10)
            elif pressed_key == "s":
                move_down(taco_image, 10)
            elif pressed_key == "d":
                move_right(taco_image, 10)


        taco_image = add_image("taco.jpg", 100)
        position_element(taco_image, "center", "center")

        keydown(move_taco)
    """

    element.style.position = "absolute"
    element.style.top = str(int(element.offsetTop) + distance) + "px"


@_is_valid_element("move_left")
def move_left(element, distance):
    """
    Moves the `element` left by the given `distance`.

    Parameters:
        - element (element): The element to move left.
        - distance (int): The distance the `element` should travel (in pixels).

    Example usage:
        def move_taco(pressed_key):
            if pressed_key == "w":
                move_up(taco_image, 10)
            elif pressed_key == "a":
                move_left(taco_image, 10)
            elif pressed_key == "s":
                move_down(taco_image, 10)
            elif pressed_key == "d":
                move_right(taco_image, 10)


        taco_image = add_image("taco.jpg", 100)
        position_element(taco_image, "center", "center")

        keydown(move_taco)
    """
    element.style.position = "absolute"
    element.style.left = str(int(element.offsetLeft) + -distance) + "px"


@_is_valid_element("move_right")
def move_right(element, distance):
    """
    Moves the `element` right by the given `distance`.

    Parameters:
        - element (element): The element to move right.
        - distance (int): The distance the `element` should travel (in pixels).

    Example usage:
        def move_taco(pressed_key):
            if pressed_key == "w":
                move_up(taco_image, 10)
            elif pressed_key == "a":
                move_left(taco_image, 10)
            elif pressed_key == "s":
                move_down(taco_image, 10)
            elif pressed_key == "d":
                move_right(taco_image, 10)


        taco_image = add_image("taco.jpg", 100)
        position_element(taco_image, "center", "center")

        keydown(move_taco)
    """

    element.style.position = "absolute"
    element.style.left = str(int(element.offsetLeft) + distance) + "px"


@_is_valid_element("move_up")
def move_up(element, distance):
    """
    Moves the `element` up by the given `distance`.

    Parameters:
        - element (element): The element to move up.
        - distance (int): The distance the `element` should travel (in pixels).

    Example usage:
        def move_taco(pressed_key):
            if pressed_key == "w":
                move_up(taco_image, 10)
            elif pressed_key == "a":
                move_left(taco_image, 10)
            elif pressed_key == "s":
                move_down(taco_image, 10)
            elif pressed_key == "d":
                move_right(taco_image, 10)


        taco_image = add_image("taco.jpg", 100)
        position_element(taco_image, "center", "center")

        keydown(move_taco)
    """

    element.style.position = "absolute"
    element.style.top = str(int(element.offsetTop) + -distance) + "px"


@_is_valid_element("play_audio")
def play_audio(element):
    """
    Plays the audio that `element` represents.

    Parameters:
        - element (element): The audio element to play.

    Example usage:

        laugh_audio = add_audio("laugh.mp3")
        play_audio(laugh_audio)
    """
    
    callback_function = create_once_callable(lambda _: element.play())

    if not element.paused:
        element.pause()
        element.currentTime = 0

    start_button = document.getElementById("start")
    # If there's a start button
    if start_button:
        # Add event listener 
        start_button.addEventListener("click", callback_function)
        # If the start button is disabled, play the sound automatically when called
        if start_button.disabled:
            element.play()
    # If there's no start button, play the sound once the page loads
    else:
        element.play()


@_is_valid_element("position_element")
def position_element(element, x, y):
    """
    Position the `element` at the given `x` and `y` position. The `x` and `y`
    arguments can be any `int`, or one of the position helpers:

    |Position | Helper1  | Helper2    | Helper3    |
    |---------|----------|------------|------------|
    |`x`      | `"left"` | `"center"` | `"right"`  |
    |`y`      | `"top"`  | `"center"` | `"bottom"` |

    Parameters:
        - element (element): The element to position.
        - x (int|str): The desired x-position of the `element`.
        - y (int|str): The desired y-position of the `element`.

    Example usage:
        taco_image = add_image("taco.jpg")
        position_element(taco_image, "center", 400)
    """

    element.style.position = "absolute"

    get_flex_align = {
        "center": "center",
        "right": "flex-end",
        "left": "flex-start",
    }

    if isinstance(x, str):
        if _is_invalid_x_position_keyword(x):
            raise Exception(
                f"""
Error in position_element()
    - '{x}' is not a valid position shortcut!
"""
            )
        element.style.alignSelf = get_flex_align[x]
    else:
        element.style.left = str(x) + "px"

    if isinstance(y, str):
        if _is_invalid_y_position_keyword(y):
            raise Exception(
                f"""
Error in position_element()
    - '{y}' is not a valid position shortcut!
"""
            )
        elif y == "bottom":
            if element.tagName == "IMG":
                element.onload = lambda _: _set_y_to_bottom(element)
            else:
                _set_y_to_bottom(element)
        elif y == "top":
            if element.tagName == "IMG":
                element.onload = lambda _: _set_y_to_top(element)
            else:
                _set_y_to_top(element)
        elif y == "center":
            if element.tagName == "IMG":
                element.onload = lambda _: _set_y_to_center(element)
            else:
                _set_y_to_center(element)
    else:
        element.style.top = str(y) + "px"


def set_background_color(color):
    """
    Sets the background color of the page to `color`.

    Parameters:
        - color (str): The desired background color.

    Example usage:
        set_background_color("darksalmon")
    """

    element = document.querySelector("html")

    if _is_invalid_color(color):
        raise Exception(
            f"""
Error in set_background_color()
    - '{color}' is not a valid color name!
"""
        )

    element.style.backgroundColor = color.lower()


@_is_valid_element("set_element_width")
def set_element_width(element, width):
    """
    Sets the `element` to the given `width`.

    Parameters:
        - element (element): The element to adjust.
        - width (int): The desired width of the `element`.

    Example usage:
        def shrink_taco():
            set_element_width(taco_image, 100)


        shrink_taco_button = add_button("Shrink Taco")
        position_element(shrink_taco_button, "center", "center")

        taco_image = add_image("taco.jpg", 300)
        position_element(taco_image, "center", 200)

        click(shrink_taco_button, shrink_taco)
    """

    element.style.width = width + "px"


@_is_valid_element("set_font_size")
def set_font_size(element, font_size):
    """
    Sets the font size of the `element` to the given `font_size`.

    Parameters:
        - element (element): The element to adjust.
        - font_size (int): The desired font size of the `element`.

    Example usage:
        def shrink_text():
            set_font_size(text_element, 25)


        shrink_text_button = add_button("Shrink Font")
        position_element(shrink_text_button, "center", "center")

        text_element = add_text("Shrink this text!", 100)
        position_element(text_element, "center", 300)

        click(shrink_text_button, shrink_text)
    """

    element.style.fontSize = str(font_size) + "px"


@_is_valid_element("set_text_color")
def set_text_color(text_element, color):
    """
    Sets the `color` of the `text_element`.

    Parameters:
        - text_element (element): The text element to adjust.
        - color (str): The desired color of the `text_element`.

    Example usage:
        red_text = add_text("This text is red", 32)
        set_text_color(red_text, "red")
    """

    if _is_invalid_color(color):
        raise Exception(
            f"""
Error in set_text_color()
    - '{color}' is not a valid color name!
"""
        )

    text_element.style.color = color


@_is_valid_element("set_text_decoration")
def set_text_decoration(text_element, decoration_string):
    """
    Sets the text decoration of the given `text_element`.

    Parameters:
        - text_element (element): The text element to adjust.
        - decoration_string (str): The decoration string for the CSS property.

    Read about different options for the decoration_string here:
        - https://developer.mozilla.org/en-US/docs/Web/CSS/text-decoration

    Example usage:
        text_element = add_text("Never Gonna Give You Up", 42)
        set_text_decoration(text_element, "underline dotted blue")
    """

    text_element.style.textDecoration = decoration_string


def set_timeout(function_to_run, time):
    """
    Runs `function_to_run` after `time` seconds.

    Parameters:
        - function_to_run (function): The function to run.
        - time (int): The time (in seconds) to wait before running the `function_to_run`.

    Example usage:
        def show_boo_text():
            boo_text = add_text("BOO!!!", 100)
            position_element(boo_text, "center", 300)


        set_timeout(show_boo_text, 3)
    """

    def _inner(fun):
        fun()

    def turn_into_callable(*args):
        _inner(function_to_run)

    callable_func = create_once_callable(turn_into_callable)

    start_button = document.getElementById("start")

    if start_button:
        start_button.addEventListener(
            "click",
            create_once_callable(lambda _: setTimeout(callable_func, time * 1000)),
        )
    else:
        setTimeout(function_to_run, time * 1000)


def set_interval(function_to_run, time):
    """
    Runs `function_to_run` every `time` seconds.

    Parameters:
        - function_to_run (function): The function to run.
        - time (int): The time (in seconds) to wait before running the `function_to_run`.

    Example usage:
        def create_ship():
            ship = add_image("ship.png", 100)
            position_element(ship, 2000, 100)
            animate_right(ship, 2500, 10)


        set_interval(create_ship, 3)
    """

    callable_func = create_proxy(function_to_run)

    start_button = document.getElementById("start")

    if start_button:
        start_button.addEventListener(
            "click",
            create_once_callable(lambda _: setInterval(callable_func, time * 1000)),
        )
    else:
        setInterval(function_to_run, time * 1000)


@_is_valid_element("_set_y_to_bottom")
def _set_y_to_bottom(element):
    canvas = document.querySelector("#canvas")
    if canvas:
        element.style.top = str(canvas.offsetHeight - element.offsetHeight) + "px"
    else:
        element.style.top = str(window.innerHeight - element.offsetHeight) + "px"


@_is_valid_element("_set_y_to_top")
def _set_y_to_top(element):
    element.style.top = "0px"


@_is_valid_element("_set_y_to_center")
def _set_y_to_center(element):
    canvas = document.querySelector("#canvas")
    if canvas:
        element.style.top = (
            str((canvas.offsetHeight / 2) - (element.offsetHeight / 2)) + "px"
        )
    else:
        element.style.top = (
            str((window.innerHeight / 2) - (element.offsetHeight / 2)) + "px"
        )


@_is_valid_element("_translate_x")
def _translate_x(element, distance, time=None):
    def _translate():
        """We need this to ensure that transforms run in interval timers."""
        element.style.transform = f"translateX({distance}px)"

    element.start_time = Date.now()
    callback_function = create_once_callable(_translate)
    setTimeout(callback_function, 50)


@_is_valid_element("_translate_y")
def _translate_y(element, distance):
    def _translate():
        element.style.transform = f"translateY({distance}px)"

    element.start_time = Date.now()
    callback_function = create_once_callable(_translate)
    setTimeout(callback_function, 50)


@_is_valid_element("update_text")
def update_text(text_element, new_text):
    """
    Changes the text in `text_element` to the `new_text`.

    Parameters:
        - text_element (element): The element to adjust.
        - new_text (str): The new text for the `text_element`.

    Example usage:
        def update_text_element():
            update_text(text_element, "Updated text")


        text_element = add_text("Original text", 32)
        position_element(text_element, "center", 400)

        update_text_button = add_button("Update Text")
        position_element(update_text_button, "center", "center")

        click(update_text_button, update_text_element)
    """
    new_text = str(new_text)
    text_element.innerHTML = new_text.replace("\\n", "<br />")
    text_element.innerHTML = new_text.replace("\n", "<br />")
    
    if not isinstance(new_text, str):
        raise Exception(
            f"Error in update_text(), the second argument is not a valid "
            "Python string!"
        )

    text_element.textContent = new_text
    


@_is_valid_element("remove_element")
def remove_element(element):
    """
    Removes the `element` from the page.

    Parameters:
        - element (element): The element to remove.

    Example usage:
        def remove_taco():
            remove_element(taco_image)


        taco_image = add_image("taco.jpg", 200)
        position_element(taco_image, "center", 300)

        remove_taco_button = add_button("Remove Taco")
        position_element(remove_taco_button, "center", "center")

        click(remove_taco_button, remove_taco)
    """

    element.remove()


@_is_valid_element("rotate_element")
def rotate_element(element, degrees):
    """
    Rotates the `element` by the given number of `degrees`.

    Parameters:
        - element (element): The element to rotate.
        - degrees (int): The number of degrees to rotate the `element`.

    Example usage:
        def rotate_taco():
            rotate_element(taco_image, 180)


        taco_image = add_image("taco.jpg", 200)
        position_element(taco_image, "center", 300)

        rotate_taco_button = add_button("Rotate Taco")
        position_element(rotate_taco_button, "center", "center")

        click(rotate_taco_button, rotate_taco)
    """

    element.style.transform = f"rotate({degrees}deg)"


@_is_valid_element("vanish")
def vanish(element):
    """
    Removes the `element` from the page over a 1 second interval.

    Parameters:
        - element (element): The element to remove.

    Example usage:
        def vanish_taco():
            vanish(taco_image)


        taco_image = add_image("taco.jpg", 200)
        position_element(taco_image, "center", 300)

        vanish_taco_button = add_button("Vanish Taco")
        position_element(vanish_taco_button, "center", "center")

        click(vanish_taco_button, vanish_taco)
    """

    # Prevents spam clicking vanished elements.
    element.removeEventListener("click", element.click_handler)
    
    if element.style.transition:
        element.style.transition += ", opacity 1s linear"
    else:
        element.style.transition = "opacity 1s linear"

    element.style.opacity = "0"
        
    def cb():
        element.remove()

    setTimeout(create_proxy(cb), 2000)
    

