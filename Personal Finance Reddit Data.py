#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Collect relevant content through the Reddit API.
import json
import praw
# PRAW documentation:
#  https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html


# In[2]:


# IMPORTANT: enter proper access credential in the config-file;
# follow instructions in reddit_credentials_verify.ipynb
import config_reddit


# In[3]:


# establish an API connection and verify read-only access
reddit = praw.Reddit(user_agent=f"Exploration script by /u/{config_reddit.user_name}",
                     client_id=config_reddit.app_id,
                     client_secret=config_reddit.app_secret)
reddit.read_only


# In[4]:


query_subreddit = 'personalfinance'


# In[5]:


nposts = 50


# In[6]:


post_ids = []
subreddit = reddit.subreddit(query_subreddit)
for p in subreddit.hot(limit = nposts):
    post_ids.append(p.id)
# check how many posts (submissions) were collected
len(post_ids)


# In[7]:


# example post details
post_details = reddit.submission(id = post_ids[1])
print(post_details.title)
print(post_details.selftext)


# In[8]:


ncomments = 10


# In[9]:


def collect_post_data(post_id, ncomments, reddit):
    psubm = reddit.submission(id = post_id)
    pdata = {'id': post_id, 'title': psubm.title, 'text': psubm.selftext}
    
    # collect first- and second-level comments
    pcomm = []
    psubcomm = []
    psubm.comments.replace_more(limit = ncomments)
    for top_comment in psubm.comments:
        pcomm.append(top_comment.body)
        for lev2_comment in top_comment.replies:
            psubcomm.append(lev2_comment.body)
    
    # assemble the data together
    pdata['comments_lev1'] = pcomm
    pdata['comments_lev2'] = psubcomm
    
    return pdata


# In[12]:


posts_all = [collect_post_data(pid, ncomments, reddit) for pid in post_ids]


# In[13]:


file_out = f"raw_post_comment_data.json"
with open(file_out, mode='w') as f:
    f.write(json.dumps(posts_all, indent=2))


# In[ ]:




