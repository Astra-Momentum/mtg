import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle{
    property var allcards : []
    property int currentPage: 0
    property int cardsPerPage: 50
    property var selected_cards : []

    function displayedCards() {
        return allcards.slice(currentPage * cardsPerPage, (currentPage + 1) * cardsPerPage)
    }
    function get_selected_cards(){
        
        return selected_cards
    }
    function clear_selected(){
        selected_cards=[]
        for (var i=0; i<cardGridView.count;i++){
            var item = cardGridView.itemAtIndex(i)
            item.unselect()
        }
    }

    ColumnLayout {anchors.fill: parent

    GridView {
        id: cardGridView
        model: displayedCards()
        cellWidth : 210
        cellHeight : 290
        Layout.fillWidth: true
        Layout.fillHeight: true
        // width: parent.width
        // height: parent.height
        delegate: Item{
            property int borderWidth : 5
            width: cardGridView.cellWidth - 10
            height: cardGridView.cellHeight - 10
            layer.enabled: true
            function unselect(){
                card.selected=false
            }
            Card {
                id:card
                name:modelData.name
                width: card.selected ? parent.width-borderWidth : parent.width
                height: card.selected ? parent.width-borderWidth : parent.width
                front_url: modelData.front !== undefined ? "../." +modelData.front : "../../images/default/cardfront.png"
                back_url: modelData.back !== undefined ? "../." +modelData.back : "../../images/default/cardback.png"
            }
            Rectangle {
                width: parent.width
                height: parent.height
                color: "transparent"
                border.color: "green"
                border.width: card.selected ? borderWidth : 0
            }
            MouseArea {
                acceptedButtons: Qt.LeftButton | Qt.RightButton
                anchors.fill: parent
                onClicked: {
                if (mouse.button === Qt.LeftButton) {
                    card.selected=!card.selected
                    var temp = {"name":modelData.name,"front":modelData.front,"back":modelData.back}
                    if (card.selected){selected_cards.push(temp)}
                    else {
                        for (var i = 0; i < selected_cards.length; i++) {
                            if(selected_cards[i].name===card.name){
                                selected_cards.splice(i, 1);
                                break;}
                        }
                    }
                    

                } else if (mouse.button === Qt.RightButton) {
                    card.flipped = !card.flipped
                }
                }
            }

        }
        }

    RowLayout{
        Button {text:"<";onClicked:{
                    if (currentPage > 0) {
                        currentPage--
                    }
                }
                enabled: currentPage > 0
            }
        Button {text:">";onClicked: {
                    if ((currentPage + 1) * cardsPerPage <allcards.length) {
                        currentPage++
                    }
                }
                enabled: (currentPage + 1) * cardsPerPage <allcards.length
        }
    Layout.alignment: Qt.AlignBottom}
    }
}