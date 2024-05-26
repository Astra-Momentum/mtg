import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Flipable{
    property string front_url
    property string back_url
    property string name
    property bool flipped: false
    property bool selected: false
    property bool dragable: false

    id: flipable
    anchors.fill: parent

    front: Image { source: front_url; anchors.fill: parent; fillMode: Image.PreserveAspectFit }
    back: Image { source: back_url; anchors.fill: parent; fillMode: Image.PreserveAspectFit }

    transform: Rotation {
        id: rotation
        origin.x: flipable.width/2
        origin.y: flipable.height/2
        axis.x: 0; axis.y: 1; axis.z: 0     // set axis.y to 1 to rotate around y-axis
        angle: 0    // the default angle
    }

    states: State {
        name: "back"
        PropertyChanges { target: rotation; angle: 180 }
        when: flipable.flipped
    }

    transitions: Transition {
        NumberAnimation { target: rotation; property: "angle"; duration: 1000 }
    }

    MouseArea {
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        anchors.fill: parent
        onClicked: flipable.flipped = !flipable.flipped
    }
}