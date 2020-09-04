import QtQuick 2.9
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import org.kde.kirigami 2.12 as Kirigami
import Mycroft 1.0 as Mycroft

Mycroft.Delegate {
    skillBackgroundSource: Qt.resolvedUrl("background.jpg")

    Image {
        anchors.centerIn: parent
        anchors.margins: Kirigami.Units.largeSpacing
        source: "correct.png"
    }
}