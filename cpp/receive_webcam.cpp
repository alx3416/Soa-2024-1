#include "ecal_interface.h"

int main(int argc, char *argv[]) {

    // Subscribers names
    eCALIO::InputInterface<pb::image> imageSubscriber;

    cv::Mat frame;

    for (;;) {
        if (imageSubscriber.receiveMessage()) {
            frame.create(imageSubscriber.message.height(), imageSubscriber.message.width(), CV_8UC3);
            frame.data = (uchar*)imageSubscriber.message.data().data();
            cv::imshow("Received Image", frame);
        }

        if (cv::waitKey(30) >= 0)
            break;
    }

    return 0;
}
