# saucedemo-ui-playwright

playwright test suite against saucedemo.com, the demo site sauce labs built
specifically for people practicing browser automation on. tests the real
ui end to end, login, cart, checkout, driving an actual browser instead of
just calling an api.

## what this is showing

driving a real browser through a full, multi step user flow, and doing it
across more than one browser at once. login, add to cart, remove from
cart, and a complete checkout that actually checks the price math adds up.

```
saucedemo-ui-playwright/
├── .github/workflows/tests.yml   # ci, installs both browsers and uploads failure evidence
├── pages/
│   ├── base_page.py              # shared stuff every page object needs
│   ├── login_page.py
│   ├── inventory_page.py         # the product listing, add to cart happens here
│   ├── cart_page.py
│   └── checkout_page.py          # all 3 checkout steps, theyre one flow
├── tests/
│   ├── test_login.py
│   ├── test_cart.py
│   ├── test_checkout.py
│   └── test_problem_user.py      # tests that catch 2 real bugs on saucedemos own broken test account
├── conftest.py                    # fixtures, login helper, page objects
├── pytest.ini
└── requirements.txt
```

## the page object pattern

every screen on the site gets its own class that knows that screens
locators and actions. tests never touch a css selector directly, they just
call things like `login_page.login(username, password)` or
`inventory_page.add_to_cart("sauce-labs-backpack")`. if saucedemo ever
changes how a button is built, i fix it in one page object instead of in
every single test that clicks that button.

## running it

```bash
pip install -r requirements.txt
playwright install chromium firefox
pytest
```

run the whole suite across both browsers, in parallel, in one go:

```bash
pytest -n auto --browser chromium --browser firefox
```

`-n auto` comes from pytest-xdist, it splits the tests across however many
cpu cores are available. `--browser` can be passed more than once,
pytest-playwright then runs the entire suite once per browser listed.

## what happens when a test fails

pytest.ini turns on a screenshot, a video, and a full playwright trace for
any test that fails, and only for tests that fail, so passing runs dont
fill up with useless files. this is the real advantage of testing a ui
over testing an api, when something breaks you actually get to see what
the browser was looking at.

## a couple of tests are meant to fail

saucedemo ships a few broken test accounts on purpose, `problem_user` is
one of them. `test_problem_user.py` asserts the same correct behavior the
other tests expect from `standard_user`, all product images should be
different, sorting z to a should reverse the list, and both genuinely
fail against `problem_user`, because both things are actually broken on
saucedemos own side. thats not a bug in this suite, its 2 real bugs this
suite actually caught. in ci these run as their own step with
`continue-on-error` set, so the real failure still happens and still
gets a real screenshot, video, and trace, without turning the whole
workflow red.

## ci

`.github/workflows/tests.yml` installs both browsers, runs the full suite
across chromium and firefox in parallel, and uploads whatever landed in
`test-results/` as a build artifact, pass or fail. that means a failing
test can be debugged straight from the github actions run, no need to
reproduce it locally first.

## test accounts

saucedemo publishes its own test accounts right on the login page,
`standard_user` for a normal login and `locked_out_user` for testing the
locked out flow. password is `secret_sauce` for all of them, its meant to
be used this way, not a secret i found.
