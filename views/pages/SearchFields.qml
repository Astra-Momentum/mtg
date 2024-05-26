import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import SearchModel



ColumnLayout{
    
    function getParams() {
        var search_params = {};
        for (var i = 0; i < repeater.count-2; i++) {
            var item = repeater.itemAt(i);
            search_params[item.param] = item.value;
        }
        return search_params;
    }
    function reset() {
        for (var i = 0; i < repeater.count; i++) {
            var item = repeater.itemAt(i);
            item.clear();
        }
    }
    function deck(){
        return repeater.itemAt(repeater.count-2).value
    }
    function amount(){
        return repeater.itemAt(repeater.count-1).value
    }
    width:parent.width
    height: parent.height
    property var params
    Repeater {
        id:repeater
        model:params
        RowLayout{
            property string param:modelData.param
            property string value:""
            Label{text:modelData.label}
            TextField{
                id: textField
                Layout.fillWidth: true
                placeholderText: modelData.param
                text: value
                onTextChanged: {
                    value=text
                }
            }
            function clear(){
                textField.text=""
            }
        }
    }
    
}

