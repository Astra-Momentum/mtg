import QtQuick 2.15
import QtQuick.Controls 2.15

Page {

    MouseArea {
        id: table
        anchors.fill: parent

        onPositionChanged: {
            if (card.dragging) {
                card.x = mouse.x - card.width / 2
                card.y = mouse.y - card.height / 2
            }
        }
    }

    Rectangle {
        id: card
        Card{
            front_url:"../../images/default/giraffe.png"
            back_url:"../../images/default/cardback.png"
        }
        width: 100
        height: 150
        visible: true
        color:"transparent"
        property bool dragging: false
        MouseArea {
            anchors.fill: parent
            drag.target: parent

            onPressed: {
                parent.dragging = true
            }

            onReleased: {
                parent.dragging = false
            }
        }
    }

}
