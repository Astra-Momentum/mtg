import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import SearchModel

Page{
    id:page
    SearchModel { id: model }
    Component.onCompleted: {
        searchfields.params = model.params
        search_results.allcards = model.results
    }

    ColumnLayout{
        anchors.fill:parent
    
    SearchFields{
        id:searchfields
        
        Layout.preferredWidth: parent.width/2
        Layout.maximumWidth: parent.width/2
        Layout.minimumWidth: parent.width/2
        // Layout.preferredHeight: parent.height/3
        // Layout.maximumHeight: parent.height/3
        // Layout.minimumHeight: parent.height/3
        Layout.alignment: Qt.AlignCenter
    }
    RowLayout{
        Layout.alignment: Qt.AlignCenter
        Button{ text:buttonText("Reset"); onClicked:{
            searchfields.reset()
            search_results.cards = []
        }}
        Button{ text:buttonText("Search"); onClicked:{
            var search_params = searchfields.getParams()
            model.search(search_params)
            search_results.allcards = model.results
        }}
        Button{ text:buttonText("Save"); onClicked:{
            var deck = searchfields.deck()
            var amount = searchfields.amount()
            var selected_cards = search_results.get_selected_cards()
            console.log(selected_cards)
            model.save(deck,selected_cards,amount)
            search_results.clear_selected()
        }}
    }
    CardsGrid{
        id: search_results
        Layout.alignment: Qt.AlignBottom
        Layout.fillWidth: true
        Layout.fillHeight: true
        allcards : []
    }
}

}