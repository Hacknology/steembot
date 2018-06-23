from steem import Steem
from steem.post import Post
import requests, json
from bs4 import BeautifulSoup
import wikipedia
from multiprocessing.pool import ThreadPool
from random_words import RandomWords
from steem.account import Account
class SteemBot(object):
    def __init__(self):
        self.s = Steem()

    def get_links(self, acc):
            r = requests.get('https://steemit.com/@{}'.format(acc))
            self.soup = BeautifulSoup(r.text, 'lxml')
            self.data = json.loads(self.soup.find_all('script', attrs={'type' : 'application/json', 'data-iso-key' : '_0'})[0].get_text())
            self.posts = self.data['global']['accounts'][acc]['blog']
            self.posts = list(
                    map(
                    lambda n: '@' + n, self.posts
                    )
            )
            return self.posts

    def send_links(self, to_acc, amount, link, user):
            self.s.commit.transfer(
                to_acc,
                amount,
                "SBD",
                memo=link,
                account=user)

    def upVote(self, user):
        #self.current_link = get_links(user)
        for i in self.get_links(user):
            print(i)
            i = i.replace("@", "")
            print(i)
            self.linked = i
            self.s.vote(self.linked, 100)
            print("[*]Voted!")

    def get_articles(self):
        pool = ThreadPool(processes=1)
        mapl = lambda fnc, *itr: list(map(fnc, *itr))

        def thread(fnc):
            def wrapper(*args):
                return (pool.apply_async(fnc, args).get ())
            return (wrapper)

        @thread
        def wiki_parser (title): 
            return (wikipedia.page (title))
        try:
        	return mapl(lambda title: wiki_parser (title).content, wikipedia.random (pages=2))
        except:
        	print('an error has occured...')
        	raise

    def post_it(self, user):
        rw,dorks_list = RandomWords(),[]
        self.kelime = rw.random_words(count=100)
        self.text = "\n".join(word for word in self.kelime)
        try:
        		self.s.post(title='Articles', body=self.text, author=user, tags=['Helloworld'], self_vote=False)
        		print('Articles has posted by', user)
        except:
        	pass
if __name__ == '__main__':
	steembot = SteemBot()
	poster_acc = ["bestdmaniamemes"]
	voter_acc = ["bestdmaniamemes"]
	to_ac = []
	amount = ""

	for user in voter_acc	:
		print("Now the active account is:", user)
		try:
			steembot.upVote(user)
			print('Voting is completed for the account named:', user)
		except:
			pass
	for poster in poster_acc:
		print("Now I'm ready to post something with,", user)
		steembot.post_it(poster)
		#print("Buying some upvote...")
		#for buyer in to_ac:
			#for link in steembot.get_links(poster):
				#steembot.send_links(buyer, amount, link, poster)

	
	
	#vote = steembot.post_it('bestdmaniamemes')