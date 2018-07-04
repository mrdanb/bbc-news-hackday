import tweepy
import requests
import os
import xmltodict
import textrazor

class NewsStory:
    para_1 = ""
    para_2 = ""
    para_3 = ""
    para_4 = ""

    def __init__(self, cps_id, short_name,
                 summary, share_url, body,
                 img_url):
        self.cps_id = cps_id
        self.short_name = short_name
        self.summary = summary
        self.share_url = share_url
        self.body = body
        self.img_url = img_url

    def parse_body(self):
        xml_dict = xmltodict.parse(self.body)
        paragraphs = xml_dict['body']['paragraph']

        self.para_1 = paragraphs[0].get('#text')
        self.para_2 = paragraphs[1]
        self.para_3 = paragraphs[2]
        self.para_4 = paragraphs[3]

        textrazor.api_key = "abbc3e1eaf816091e23bac911827701fea30ecd01395144984c46f59"
        client = textrazor.TextRazor(extractors=["entities", "topics", "phrases", "words"])
        client.set_cleanup_mode("stripTags")
        client.set_classifiers(["textrazor_newscodes"])

        response = self.client.analyze(self.summary + self.para_1 + self.para_2 + self.para_3 + self.para_4)

        for topic in response.topics():
            if topic.score > 0.8:
                print(topic.label)

        for np in response.noun_phrases():
            print(np.words[0].input_start_offset)
            print(np.words[-1].input_end_offset)


class TrevorRequest:
    trevor_base_url = "http://trevor-producer-cdn.api.bbci.co.uk/content/"
    most_popular_url = trevor_base_url + "most_popular/news"

    def get_most_popular_cps_id(self):
        most_popular_json = requests.get(self.most_popular_url).json()
        first_relation = most_popular_json.get('relations')[0].get('content')
        return first_relation.get('id')

    def create_cps_index(self, cps_id):
        cps_json = requests.get(self.trevor_base_url + cps_id).json()
        short_name = cps_json.get('shortName')
        summary = cps_json.get('summary')
        share_url = cps_json.get('shareUrl')
        body = cps_json.get('body')
        img_url = cps_json['relations'][0]['content'].get('href')

        return NewsStory(cps_id, short_name, summary, share_url, body, img_url)


class TwitterHandler:
    auth = tweepy.OAuthHandler("pR3JDWZSJGtAPNK6X1VPxRpVu",
                               "MVxGRv7Hl59mjNeuQ3QjWhtPrFL8bD9iQM3bVvuyzvGiwjcUCX")
    auth.set_access_token("1014109820385939456-JIX4nPJ4IIMzxSvUNWvEH5MgF2wrxn",
                          "qw87e6otiwYBbEIrLzRzGbwAHmkALmZ0JfR1l47rNmBxL")

    api = tweepy.API(auth)
    public_tweets = api.home_timeline()

    def build_tweets(self, news_story):
        return [
            '{}. #BBCInBrief \n • {}'.format(
                news_story.short_name, news_story.para_1),
            '• {} \n \n • {}'.format(news_story.para_2, news_story.para_3),
            '• {} \n {}'.format(news_story.para_4, news_story.share_url)
        ]

    def download_image(self, news_story):
        filename = 'temp_img.jpg'
        img_request = requests.get(news_story.img_url, stream=True)

        if img_request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in img_request:
                    image.write(chunk)
                return filename
        else:
            print('Unable to download image')
            return None

    def post(self, news_story):
        reply_id = None
        posts = self.build_tweets(news_story)
        img = self.download_image(news_story)

        for post in posts:
            if img and not reply_id:
                status = self.api.update_with_media(img, post)
                os.remove(img)
            elif reply_id:
                status = self.api.update_status(post, reply_id)
            else:
                status = self.api.update_status(post)
            reply_id = status.id


if __name__ == '__main__':
    request = TrevorRequest()
    cps_id = request.get_most_popular_cps_id()
    story = request.create_cps_index(cps_id)
    story.parse_body()
    #twitter = TwitterHandler()
    #twitter.post(story)