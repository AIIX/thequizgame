import QtQuick 2.9
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import org.kde.kirigami 2.12 as Kirigami
import Mycroft 1.0 as Mycroft

Mycroft.Delegate {
    skillBackgroundSource: Qt.resolvedUrl("background.jpg")
    
    Rectangle {
        id: questionask
        color: Qt.rgba(0, 0, 0, 0.5)
        radius: 10
        
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.topMargin: Kirigami.Units.largeSpacing
        
        height: questiondisplay.contentHeight
        border.width: 1
        border.color: Qt.rgba(0.3, 0.3, 0.3, 0.5)
        
        Kirigami.Heading {
            id: questiondisplay
            width: parent.width
            wrapMode: Text.WordWrap
            level: 1
            horizontalAlignment: Text.AlignHCenter
            text: sessionData.question
        }
    }
    
    ColumnLayout {
        id: answersview
        anchors.top: questionask.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        
        Repeater {
            model: sessionData.answer_list
            
            Button {
                id: answerbox
                Layout.fillWidth: true
                Layout.margins: Kirigami.Units.largeSpacing
                Layout.minimumHeight: answertext.contentHeight + Kirigami.Units.largeSpacing
                
                background: Rectangle {
                    color: Qt.rgba(0, 0, 0, 0.5)
                    radius: 10
                    border.width: 1
                    border.color: Qt.rgba(0.3, 0.3, 0.3, 0.5)
                }
                
                contentItem: Kirigami.Heading {
                    id: answertext
                    width: parent.width
                    wrapMode: Text.WordWrap
                    level: 2
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    text: modelData
                }
                
                onClicked: {
                    triggerGuiEvent("quiz-game.jz.answer", {"utterance": modelData})
                }
            }
        }
    }
}
