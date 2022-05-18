
#エッジ検出を行うアプリ
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import cv2

st.title("動画からエッジ検出を行うアプリ")#タイトルを表示
st.write("アプリケーション化")#文章をページに記入する


class VideoProcessor:
  #スライダーの初期位置を定義
    def __init__(self) -> None:
        self.threshold1 = 100
        self.threshold2 = 200

  #recv()は画像フレームを受け取り、画像フレーム返す
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        #ここに画像処理を行うコードを記述
        #cv2.Canny(img, 100, 200)はエッジ検出フィルタ
        #cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)はグレースケールをBGRに戻す
        img = cv2.cvtColor(cv2.Canny(img, self.threshold1, self.threshold2), cv2.COLOR_GRAY2BGR)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

#webrtc_streamer:webブラウザを介した映像・音声の入出力を扱うコンポーネント
ctx = webrtc_streamer(    
    key="example",
    video_processor_factory=VideoProcessor,
    #サーバがローカルにない場合、映像・音声伝送の通信を確立するために設定
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
)
if ctx.video_processor:
  #st.slider():スライダーを作る組み込みウィジェット
    ctx.video_processor.threshold1 = st.slider("Threshold1", min_value=0, max_value=1000, step=1, value=100)
    ctx.video_processor.threshold2 = st.slider("Threshold2", min_value=0, max_value=1000, step=1, value=200)