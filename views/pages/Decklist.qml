import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

import DeckListModel

Page {
    DeckListModel { id: model }

    GridView {
        id:gridView
        anchors.centerIn: parent
        cellWidth : 200
        cellHeight : cellWidth
        height : parent.height
        width : cellWidth*Math.floor(parent.width / cellWidth)

        model: model
        delegate: Button {
            text: name
            anchors.margins: 10
            width: gridView.cellWidth-10; height: gridView.cellWidth-10
            background:Image {
                fillMode: Image.PreserveAspectCrop
                source: "../../images/default/deck.jpg"}
            onClicked: loader.setSource("Deck.qml",{"deckName":name, "deckFile":file})
            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.RightButton
                onClicked: openContextMenu(index, name, file)
            }
        }
    }

    Row {
        anchors.bottom: parent.bottom
        spacing: 10
        Button {
            text: buttonText("New Deck")
            onClicked: model.newDeck()
        }
    }

    Component {
        id: menu;
        Menu {
        property int index
        property string name
        property string file
        id: contextMenu
        MenuItem {
            text: buttonText("Open")
            onTriggered: loader.setSource("Deck.qml",{"deckName":name, "deckFile":file})
        }
        MenuItem {
            text: buttonText("Copy")
            onTriggered: model.copyDeck(index)
        }
        MenuItem {
            text: buttonText("Rename")
            onTriggered: openDialog(index, name)
        }
        MenuItem {
            text: buttonText("Delete")
            onTriggered: model.deleteDeck(index)
        }
        }
    }

    Component {
        id: dialog;
        Dialog {
            id: renameDialog
            property int index
            property string oldName
            title: "Renaming Deck"
            anchors.centerIn: parent
            modal: true
            TextField{
                id:input
                width: parent.width
                placeholderText: oldName
            }
            standardButtons: Dialog.Ok | Dialog.Cancel
                onAccepted: model.renameDeck(input.text,index)
                onRejected: console.log("Cancel clicked")
        }
    }

    MessageDialog {
        id: messageDialog
        title: "Error"
        text: "Failed to rename deck, another deck already have the same name"
    }

    function openContextMenu(index, name, file) {
        var contextMenu = menu.createObject(gridView,{
            "index":index,
            "name":name,
            "file":file
        })
        contextMenu.popup();
    }

    function openDialog(index, name) {
        var renameDialog = dialog.createObject(gridView,{
            "index":index,
            "oldName":name,
        })
        renameDialog.open();
    }
}

