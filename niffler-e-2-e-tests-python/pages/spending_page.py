import time

from selene import browser, be, have, query


class SpendingPage:
    def __init__(self):
        self.history = browser.element('.main-content__section-history h2')
        self.statistics = browser.element('//*[@id="stat"]/h2')
        self.new_spending = browser.element("#react-select-3-placeholder")
        self.spending_container = browser.element('.table.spendings-table td')
        self.amount = browser.element('input[name=amount]')
        self.currency = browser.element('input[name=currency]')
        self.category = browser.element('#react-select-3-input')
        self.spend_date = browser.element('.calendar-wrapper  input[type="text"]')
        self.description = browser.element('input[name=description]')
        self.add_button = browser.element('button[type=submit]')
        self.error_message = browser.element('.add-spending__form .form__error')
        self.checkbox_for_all = browser.element('thead input[type="checkbox"]')
        self.button_delete = browser.element('.spendings__bulk-actions .button_type_small')
        self.successful_delete = browser.element('.Toastify__toast-body div:nth-child(2)')
        self.no_spends = browser.element('.main-content__section-history > div > div:nth-child(3)')

    def check_spending_page_titles(self):
        browser.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.history.should(have.text('History of spendings'))

    def create_spending(self, amount: int, currency: str, category: str, description: str = None, spend_date: str = None):
        self.amount.clear().should(be.blank).type(amount)

        if currency and currency != "RUB":
            browser.element('div[id="currency"]').click()
            browser.element(f'.MuiButtonBase-root[data-value="{currency}"]').click()
        time.sleep(2)
        self.category.type(category).press_enter()

        if spend_date:
            self.spend_date.set_value(spend_date)

        if description:
            self.description.should(be.blank).type(description)

        self.add_button.click()

    def check_spending_exists(self, category, amount):
        filtered_cells = browser.all('.table.spendings-table td').filtered_by(have.text(f'{category} {amount}'))

        for cell in filtered_cells:
            print(f"Найдена ячейка с текстом: {cell.get(query.text)}")

    def check_delete_spending(self):
        browser.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.checkbox_for_all.should(be.visible).click()
        self.button_delete.click()
        self.no_spends.should(have.text('No spendings provided yet!'))



    def check_category_error_message(self):
        self.error_message.should(have.text('Category is required'))

    def check_amount_error_message(self):
        self.error_message.should(have.text('Amount should be greater than 0'))

    def check_date_error_message(self):
        self.error_message.should(have.text('You can not pick future date'))

spending_page = SpendingPage()