from selene import browser, have, be


class ProfilePage:

    def __init__(self):
        self.input_category = browser.element('.add-category__input-container .form__input')
        self.button_add_category = browser.element('.add-category__input-container button')
        self.successful_alert =  browser.element('div[role="alert"] div:nth-child(2)')
        self.error_alert = browser.element('.add-category__input-container button')
        self.firstname = browser.element('[name="firstname"]')
        self.surname = browser.element('[name="surname"]')
        self.button_submit = browser.element('[type="submit"]')
        self.person_icon = browser.element('[data-testid="PersonIcon"]')
        self.profile = browser.element('//li[.="Profile"]')
        self.category_name = lambda name_category: browser.element(f'//span[.="{name_category}"]').should(
            have.text(f"{name_category}"))
        self.category_name_in_profile = browser.element('.categories__list li:nth-child(1)')
        self.name = browser.element('input[name=category]')
        self.category_name = lambda name: browser.all('span.MuiChip-label.MuiChip-labelMedium.css-14vsv3w').element_by(
            have.text(name))
        self.category_input = lambda name: browser.element(f'input[value="{name}"]')
        self.parent_element = browser.all('div:has(span.MuiChip-label.MuiChip-labelMedium.css-14vsv3w)')
        self.archive_button = 'button[aria-label="Archive category"]'
        self.confirm_archive = browser.all('button[type=button]').element_by(have.text('Archive'))
        self.archived_button = browser.element('//span[.="Show archived"]')
        self.archived_category = lambda name: browser.all(
            'span.MuiChip-label.MuiChip-labelMedium.css-14vsv3w').element_by(
            have.text(name))

    def successful_adding(self):
        self.successful_alert.should(have.text('New category added'))

    def check_adding_category(self, category):
        self.input_category.type(category)
        self.button_add_category.click()


    def check_error_message(self):
        self.successful_alert.should(have.text('Can not add new category'))

    def check_adding_empty_name_category(self):
        self.input_category.type('')
        self.button_add_category.click()
        self.check_error_message()

    def check_filling_form(self, name, surname):
        self.firstname.set_value(name)
        self.surname.set_value(surname)
        browser.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.button_submit.click()

        self.successful_alert.should(have.text('Profile successfully updated'))


    def category_should_be_exist(self, name_category: str) -> None:
        self.person_icon.click()
        self.profile.click()
        self.category_name(name_category).click()

    @staticmethod
    def refresh_page() -> None:
        browser.driver.refresh()

    def edit_category_name(self, old_name: str, new_name: str) -> None:
        self.category_name_in_profile(old_name).should(be.present).click()
        self.category_input(old_name).clear().should(be.blank).type(new_name)
        self.category_input(new_name).press_enter()

    def archive_category(self, category_name: str) -> None:
        self.parent_element.element_by(have.text(category_name)).element(self.archive_button).click()
        self.confirm_archive.click()

    def should_be_category_name(self, name: str) -> None:
        self.category_name_in_profile(name).should(be.present)

    def check_archived_category(self, name: str) -> None:
        self.archived_button.click()
        self.archived_category(name)

profiles_page = ProfilePage()
