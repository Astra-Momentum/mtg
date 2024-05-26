import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    property string language: "fr"

    visible: true
    width: 600
    height: 300

    title: "MTG mange ta giraffe"

    background: Image{
        fillMode: Image.PreserveAspectCrop
        source: "../images/default/background.jpg"
    }

    header: ToolBar {
        RowLayout {
        anchors.fill: parent
        MenuBarItem { text:buttonText("Home"); onClicked:loader.setSource("pages/Home.qml")}
        MenuBarItem { text:buttonText("Play"); onClicked:loader.setSource("pages/Table.qml") }
        MenuBarItem { text:buttonText("Decks"); onClicked:loader.setSource("pages/Decklist.qml") }
        MenuBarItem { text:buttonText("Search Cards"); onClicked:loader.setSource("pages/Search.qml") }
        MenuBarItem { text:buttonText("Settings"); onClicked:loader.setSource("pages/ToDo.qml") }
        MenuBarItem { text:buttonText("About"); onClicked:loader.setSource("pages/ToDo.qml") }
        MenuBarItem { text:buttonText("Load Cards"); onClicked:loader.setSource("pages/ToDo.qml") }
        Rectangle   { Layout.fillWidth: true }
        MenuBarItem { text:buttonText("Language"); onClicked:language = (language === "en") ? "fr" : "en"; }
        MenuBarItem { text:buttonText("Quit"); onClicked:Qt.quit()}
        }
    }

    Loader {
        id: loader
        anchors.fill: parent
        source: "pages/Home.qml"
    }

    Connections{
        target: loader.item
    }

    function buttonText(key) {
        var translations = {
        "About": {"en": "About", "fr": "À propos"},
        "Blue": {"en": "Blue", "fr": "Bleu"},
        "Black": {"en": "Black", "fr": "Noir"},
        "Color": {"en": "Color", "fr": "Couleur"},
        "Colorless": {"en": "Colorless", "fr": "Colorless"},
        "Copy": {"en": "Copy", "fr": "Copier"},
        "Cost": {"en": "Cost", "fr": "Cout"},
        "Deck": {"en": "Deck", "fr": "Deck"},
        "Decks": {"en": "Decks", "fr": "Decks"},
        "Delete": {"en": "Delete", "fr": "Supprimer"},
        "Folder": {"en": "Folder", "fr": "Fichier"},
        "FolderList": {"en": ["Regular", "Double", "Any"], "fr": ["Simple", "Double", "Toutes"]},
        "Green": {"en": "Green", "fr": "Vert"},
        "Home": {"en": "Home", "fr": "Accueil"},
        "Language": {"en": "Français", "fr": "English"},
        "Load Cards": {"en": "Load Cards", "fr": "Charger des cartes"},
        "Name": {"en": "Name", "fr": "Nom"},
        "New Deck": {"en": "New Deck", "fr": "Nouveau Deck"},
        "Open": {"en": "Open", "fr": "Ouvrir"},
        "Play": {"en": "Play", "fr": "Jouer"},
        "Quit": {"en": "Quit", "fr": "Quitter"},
        "Rarity": {"en": "Rarity", "fr": "Rarity"},
        "RarityList": {"en": ["Common", "Uncommon", "Rare", "Mythic"], "fr": ["Common", "Uncommon", "Rare", "Mythic"]},
        "Red": {"en": "Red", "fr": "Rouge"},
        "Rename": {"en": "Rename", "fr": "Renommer"},
        "Reset": {"en": "Reset", "fr": "Réinitialiser"},
        "Save": {"en": "Save", "fr": "Enregistrer"},
        "Search": {"en": "Search", "fr": "Rechercher"},
        "Search Cards": {"en": "Search Cards", "fr": "Rechercher des cartes"},
        "Set": {"en": "Set", "fr": "Set"},
        "Settings": {"en": "Settings", "fr": "Paramètres"},
        "Type": {"en": "Type", "fr": "Type"},
        "White": {"en": "White", "fr": "Blanc"}
        }
        return translations[key][language]
    }

}
