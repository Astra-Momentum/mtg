import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import CardListModel

Page {
    property string deckName
    property string deckFile
    CardListModel { id: model }

    Component.onCompleted: { model.loadCards(deckFile) }

    GridView {
        header: Label { text: deckName; font.bold: true; font.pointSize: 16 }
        id: gridView
        anchors.centerIn: parent
        cellWidth : 210
        cellHeight : 290
        height : parent.height
        width : cellWidth*Math.floor(parent.width / cellWidth)
        model : model
        delegate: Item{
            width: gridView.cellWidth - 10
            height: gridView.cellHeight - 10
            Card{
                front_url: model.front
                back_url: model.back !== undefined ? model.back : "../../images/default/cardback.png"
            }
            Badge{
                    text: model.amount.toString()
                    visible: model.amount > 1
            }
        }
    }
}
