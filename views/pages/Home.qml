import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

Item {
    ColumnLayout{
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter

        Button{ text:buttonText("Play"); onClicked:loader.setSource("Table.qml"); Layout.fillWidth: true }
        Button{ text:buttonText("Decks"); onClicked:loader.setSource("Decklist.qml"); Layout.fillWidth: true }
        Button{ text:buttonText("Search Cards"); onClicked:loader.setSource("Search.qml"); Layout.fillWidth: true }
        Button{ text:buttonText("Settings"); onClicked:loader.setSource("Page1.qml"); Layout.fillWidth: true }
        Button{ text:buttonText("About"); onClicked:loader.setSource("Page1.qml"); Layout.fillWidth: true }
        Button{ text:buttonText("Load Cards"); onClicked:loader.setSource("Page1.qml"); Layout.fillWidth: true }
        Button{ text:buttonText("Quit"); onClicked:Qt.quit(); Layout.fillWidth: true }
    }
} 