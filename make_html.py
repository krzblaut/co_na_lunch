from doki import DokiMenu
from otwarte import OtwarteMenu
from drukarnia import DrukarniaMenu
from noz import NozMenu
from shamo import ShamoMenu


class CreateHTML:

    html_template = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>Table Example</title>
            </head>
        <body>
            <table>
                {menu_table}
            </table>
        </body>
        </html>"""
    

    def __init__(self):
        pass


    def make_menu_table(self):
        menu_table = [['Lokal', 'Menu']]
        doki = DokiMenu()
        doki_lunch = doki.get_todays_menu()
        menu_table.append(['Doki', doki_lunch])
        otwarte = OtwarteMenu()
        otwarte_lunch = otwarte.get_todays_menu()
        menu_table.append(['Otwarte Drzwi   ', otwarte_lunch])
        drukarnia = DrukarniaMenu()
        drukarnia_lunch = drukarnia.get_todays_menu()
        menu_table.append(['Drukarnia', drukarnia_lunch])
        noz = NozMenu()
        noz_lunch = noz.get_todays_menu()
        menu_table.append(['NÕŻ', noz_lunch])
        shamo = ShamoMenu()
        shamo_lunch = shamo.get_todays_menu()
        menu_table.append(['Shamo', shamo_lunch])
        return menu_table
    
    
    def generate(self):
        menu_table = self.make_menu_table()
        table_rows = ''
        for row in menu_table:
            table_cells = ''
            for cell in row:
                table_cells += f'<td>{cell}</td>'
            table_rows += f'<tr>{table_cells}</tr>'
        html_output = self.html_template.format(menu_table=table_rows)
        return html_output
        

# html = CreateHTML()
# html.generate()