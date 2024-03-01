#include "ecal_interface.h"


int main(int argc, char *argv[]) {

    // Subscribers names
    eCALIO::ImageOutput imagePublisher;
    eCAL::Process::SleepMS(1000);

    cv::Mat frame, frame_gray;
    cv::VideoCapture cap;

    int deviceID = 0; // 0 = open default camera
    int apiID = cv::CAP_ANY; // 0 = autodetect default API
    cap.open(deviceID, apiID);
    if (!cap.isOpened()) {
        std::cerr << "ERROR! Unable to open camera\n";
        return -1;
    }
    for (;;) {
        cap.read(frame);

        if (frame.empty()) {
            std::cerr << "ERROR! blank frame grabbed\n";
            break;
        }

        cv::imshow("Live", frame);

        // Updating & send protobuf message
        imagePublisher.updateMessage(frame, pb::UNCOMPRESSED, pb::RGB);
        imagePublisher.sendMessage();
        eCAL::Process::SleepMS(5);

        if (cv::waitKey(5) >= 0)
            break;
    }
    return 0;
}