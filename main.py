
from make_html import CreateHTML

if __name__ == 'main':


    places = ['Doki', 'Drukarnia', 'Nóż', 'Otwarte drzwi']
    lunch_table = []
    

    doki = DokiMenu()
    doki_menu = doki.get_todays_menu()


    lunch_table.append(['Doki', doki_menu])


