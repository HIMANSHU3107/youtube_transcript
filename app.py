from flask import Flask, render_template, request, jsonify, make_response, abort
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import T5ForConditionalGeneration, T5Tokenizer
app = Flask(__name__)
CORS(app)

def transcript_text(video_id):
    print(video_id)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    result = ""
    for i in transcript:
        result += ' ' + i['text']
    # print(result)
    print(len(result))
    return result

    # model = T5ForConditionalGeneration.from_pretrained("t5-base")
    # tokenizer = T5Tokenizer.from_pretrained("t5-base")
    # num_ite = int(len(result)/2000)
    # summarized_text = ""
    # for i in range(0, num_ite+1):
    #     st = i * 2000
    #     end = (i+1) * 2000
    #     inputs = tokenizer.encode("summarize: " + result[st:end], return_tensors="pt", max_length=512, truncation=True)
    #     outputs = model.generate(inputs, max_length=500, min_length=100, length_penalty=2.0, num_beams=4, early_stopping=True)
    #     temp = tokenizer.decode(outputs[0])
    #     summarized_text += ' ' + temp

    # print(len(summarized_text))
    # print(summarized_text)
    # return summarized_text

def summarized_text(result, video_id):
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    num_ite = int(len(result)/2000)
    summarized_text = ""
    for i in range(0, num_ite+1):
        st = i * 2000
        end = (i+1) * 2000
        inputs = tokenizer.encode("summarize: " + result[st:end], return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(inputs, max_length=500, min_length=100, length_penalty=2.0, num_beams=4, early_stopping=True)
        temp = tokenizer.decode(outputs[0])
        summarized_text += ' ' + temp

    print(len(summarized_text))
    print(summarized_text)
    return summarized_text

# @app.route("/", methods=['GET','POST'])
# def hello_world():
#     if request.method=='POST':
#         print(request.form['videoID'])
#         youtube_video = request.form['videoID']
#         if(youtube_video.find('=') != -1):
#             video_id = youtube_video.split("=")[1]
#         else:
#             video_id = youtube_video.split("/")[3]
#         summarized_text(video_id)
#     return render_template('index.html')

@app.route('/api/summarize/<string:youtube_video>', methods=['GET'])
def YouTube_Video(youtube_video):
    transcript = transcript_text(youtube_video)
    summary = summarized_text(transcript, youtube_video)
    res = {
        "Video ID": youtube_video,
        "Transcript": transcript,
        "Summary": summary
    }
    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True)