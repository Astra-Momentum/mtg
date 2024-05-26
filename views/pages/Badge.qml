import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    property alias text: label.text
        width: 20
        height: 20
        color: "grey"
        radius: 50 // Adjust as needed
        anchors {
            top: parent.top
            right: parent.right
            margins: 5 // Adjust spacing from top and right
        }
        Label {
            id:label
        text: text
        color: "white"
        font.pixelSize: 16
        anchors.centerIn: parent
    }}