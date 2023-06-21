import requests
import pandas as pd

listeof_tweets = []



def get_code(id, code):
    params = {
        'variables': '{"userId":"' + id + '","count":100,"cursor":"' + code + '","includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true}',
        'features': '{"rweb_lists_timeline_redesign_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":false,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":false,"responsive_web_enhance_cards_enabled":false}',
    }

    req = requests.get(
        'https://twitter.com/i/api/graphql/NPgNFbBEhFTul68weP-tYg/UserTweets',
        params=params,
        headers=headers,
    )
    try:
        all_tweets = req.json()['data']['user']['result']['timeline_v2']['timeline']['instructions'][0]['entries']
        if len(all_tweets) != 2:
            for tweet in all_tweets:
                # entry id
                if 'tweet' in tweet['entryId']:
                    try:
                        # resulttype
                        text = (tweet['content']['itemContent']['tweet_results']['result']['legacy']['full_text'])
                        # number like
                        like = (tweet['content']['itemContent']['tweet_results']['result']['legacy']['favorite_count'])
                        # number retweet
                        retweet = (
                        tweet['content']['itemContent']['tweet_results']['result']['legacy']['retweet_count'])
                        # number reply
                        reply = (tweet['content']['itemContent']['tweet_results']['result']['legacy']['reply_count'])
                        # number quote
                        quote = (tweet['content']['itemContent']['tweet_results']['result']['legacy']['quote_count'])

                        listeof_tweets.append([text, like, retweet, reply, quote])
                        print(len(listeof_tweets))
                    except Exception as e:
                        pass
                elif 'cursor-bot' in tweet['entryId']:
                    # get value of cursor-bottom
                    code = tweet['content']['value']
                    get_code(id, code)
    except:
        pass


def main(id):
    params = {
        'variables': '{"userId":"' + id + '","count":20,"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true}',
        'features': '{"rweb_lists_timeline_redesign_enabled":true,'
                    '"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,'
                    '"creator_subscriptions_tweet_preview_api_enabled":true,'
                    '"responsive_web_graphql_timeline_navigation_enabled":true,'
                    '"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,'
                    '"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,'
                    '"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,'
                    '"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,'
                    '"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,'
                    '"standardized_nudges_misinfo":true,'
                    '"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":false,'
                    '"longform_notetweets_rich_text_read_enabled":true,'
                    '"longform_notetweets_inline_media_enabled":false,"responsive_web_enhance_cards_enabled":false}',
    }

    req = requests.get(
        'https://twitter.com/i/api/graphql/NPgNFbBEhFTul68weP-tYg/UserTweets',
        params=params,
        headers=headers,
    )

    all_tweets = req.json()['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries']
    for tweet in all_tweets:
        # entry id
        if 'tweet' in tweet['entryId']:
            try:
                # resulttype
                text = (tweet['content']['itemContent']['tweet_results']['result']['legacy']['full_text'])
                # number like
                like = (tweet['content']['itemContent']['tweet_results']['result']['legacy']['favorite_count'])
                # number retweet
                retweet = (tweet['content']['itemContent']['tweet_results']['result']['legacy']['retweet_count'])
                # number reply
                reply = (tweet['content']['itemContent']['tweet_results']['result']['legacy']['reply_count'])
                # number quote
                quote = (tweet['content']['itemContent']['tweet_results']['result']['legacy']['quote_count'])

                listeof_tweets.append([text, like, retweet, reply, quote])
            except Exception as e:
                pass
        elif 'cursor-bottom' in tweet['entryId']:
            # get value of cursor-bottom
            code = tweet['content']['value']
            get_code(id, code)

    # write in file using padans
    pf = pd.DataFrame(listeof_tweets, columns=['text', 'like', 'retweet', 'reply', 'quote'])
    pf.to_excel('tweets.xlsx', index=False)


if __name__ == '__main__':
    guest_token = input('Entrez votre guest token: ')
    id_of_user = input('Entrez l\'id de l\'utilisateur: ')

    headers = {
        'authority': 'twitter.com',
        'accept': '*/*',
        'accept-language': 'fr-FR,fr;q=0.9',
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs'
                         '%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'content-type': 'application/json',
        'referer': 'https://twitter.com/OG_Mihawk',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36',
        'x-guest-token': guest_token,
        'x-twitter-active-user': 'yes',
        'x-twitter-client-language': 'fr',
    }
    main(id_of_user)
