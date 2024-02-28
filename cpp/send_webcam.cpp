#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>


int main(int argc, char *argv[]) {
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

        if (cv::waitKey(5) >= 0)
            break;
    }
    return 0;
}