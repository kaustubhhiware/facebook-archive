# facebook-archive
[![forthebadge](http://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/for-you.svg)](https://forthebadge.com)

[![Chat at Slack](https://img.shields.io/badge/chat%20on%20-Slack-brightgreen.svg?style=for-the-badge)](https://girlscriptgssoc.slack.com/messages/CB4V6N62H/details/)

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=shields)](http://makeapullrequest.com) [![MIT Licence](https://badges.frapsoft.com/os/mit/mit.png?v=103)](https://opensource.org/licenses/mit-license.php) ![Python](https://img.shields.io/badge/python-2.7-blue.svg)


![GitHub open pull requests](https://img.shields.io/github/issues-pr/kaustubhhiware/facebook-archive.svg) 
![GitHub open issues](https://img.shields.io/github/issues/kaustubhhiware/facebook-archive.svg)

> Analyse everything facebook knows about you, through their own archive.

In light of the recent facebook's data breach, Mark Zuckerberg made all the data available for each user via Facebook. You're going to need to download it, we'll get to it shortly. There are some things that would take a lot of time (too costly API calls) online, but can be easily done on archived data.

## Table of Contents

* [Getting the data](#getting-the-data)
* [Usage](#usage)
  - [Friends](#friends)
  - [Messages](#messages)
* [Contributing](#contributing)
* [Features](#features)
  - [Your friends](#your-friends)
  - [Your messages](#your-messages)
* [Observations](#observations)
* [Why](#why)
* [License](#why)

## Getting the data

1. Head on to [Facebook > Settings > General Settings > Your facebook information](https://www.facebook.com/settings?tab=your_facebook_informations).
2. Select the JSON data format and click on download archive. It might take some time to prepare the archive, this might take upto 10-15 minutes. NOTE: The download might be in order of 100s MBs. Disable photo and video download options to save some bandwidth. (My archive was ~300MB).
3. If possible, downlaod the same data in HTML format. It is much easier to browse through your archive and spot some interesting patterns in the HTML format, however this is not necessary. The JSON format will suffice for processing, refer [#2](https://github.com/kaustubhhiware/facebook-archive/issues/2).
 ![](images/archive-download.png)
 
[↥ back to top](#table-of-contents)

## Usage

Install requirements with `pip install -r requirements.txt`

### Friends

```
> python plot_friends.py
Enter facebook archive extracted location: <location of extracted data folder,  e.g.: "facebook-kaustubhhiware">
```
You can also run the script on sample data included in the examples folder:
```python
> python plot_friends.py
Enter facebook archive extracted location: ./examples
```
[↥ back to top](#table-of-contents)

### Messages

**Will be updated soon**

* Plot messages across all conversations.
 ```
 > python plot_messages.py -a
 Enter facebook archive extracted location: "location of extracted, downloaded zip: like facebook-kaustubhhiware" 
 ```

* Plot messages for a single conversation.
 ```
 > python plot_messages.py
 Enter facebook archive extracted location: "location of extracted, downloaded zip: like facebook-kaustubhhiware"
 Enter id for friend: 511
 ```

What's this id? 
1. Open index.html in `facebook-yourfacebookusername`
2. Click messages. Search for the person / conversation you want to analyse.
3. Clicking on that chat should open a url like ; 'file:///home/kaustubh/GitHub/facebook-kaustubhhiware/messages/511.html'. For this particular chat, 511 is the id for this particular conversation.
[↥ back to top](#table-of-contents)

## Contributing

Your contributions are always welcome :smile: ! Please have a look at the [contribution guidelines](CONTRIBUTING.md) first.

Before working on an issue / feature, it is **crucial** that you're assigned the task on a GitHub issue.
* If a relevant issue already exists, discuss on the issue and get yourself assigned on GitHub.
* If no relevant issue exists, open a new issue and get it assigned to yourself on GitHub.
Please proceed with a Pull Request only after you're assigned. It'd be a waste of your time as well as ours if you have not contacted us before hand when working on some feature / issue.

If you are here for GirlScript's Summer of Code and wish to seek assistance, feel free to contact any of the mentors on [slack](https://girlscriptgssoc.slack.com/) - 
[@kaustubhhiware](https://girlscriptgssoc.slack.com/messages/DB0B3GBEG/), [@techytushar](https://girlscriptgssoc.slack.com/messages/DBBGEQAPQ/),
[@Anubhav](https://girlscriptgssoc.slack.com/messages/DBAK57AQ2/), [@fhackdroid](https://girlscriptgssoc.slack.com/messages/DBAK4TUP4/), [@Roopal](https://girlscriptgssoc.slack.com/messages/DB92S68SX).

[↥ back to top](#table-of-contents)

## Features

(Click to expand)

### Your friends

Plot the friends you make every day (blue), and the friends so far (orange).

 ![](images/friends-cumulative.png)

<details>
<summary>Plot exclusively the friends you make each day.</summary>

 ![](images/friends-each.png)
</details>

<details>
<summary>Plot messages as a function of month.</summary>

 ![](images/friends-month.png)
</details>

[↥ back to top](#table-of-contents)


### Your Messages

The following is available for either a specific chat (person / group) or for all messages.

Plot all messages so far, with new messages each hour.

 ![](images/msgs-cumulative.png)

<details>
<summary>Plot only new messages each hour.</summary>

 ![](images/msgs-each.png)
</details>
<details>
<summary>Plot messages as a function of hour (0-24)</summary>

 ![](images/msgs-hour.png)
</details>
<details>
<summary>Plot messages as a function of month.</summary>

 ![](images/msgs-month.png)
</details>

[↥ back to top](#table-of-contents)

### Friend Request
Plot the friends you make every day(Red) ,friend request send every day(green) and friend request received every day(blue)

![](images/FriendEachDay.png)

<details>
  <summary>Plot all the friend request received,send and total friend so far.</summary>
  </details>
 
 Compare the Friend request recieved received and friend request send.
![](images/Compare.png)
 
 <details>
  <summary>We compare monthwise no.of friend request send vs friend request received</summary>
  </details>

### Your reactions

Plot count of different reactions to posts

 ![](images/reactions_plot2.png)

<details>
<summary>Plot of 10 Friends whose posts you react to the most</summary>

 ![](images/top10_friends.png)
</details>
<details>
<summary>Plot reactions as a function of month.</summary>

 ![](images/reactions_monthwise.png)
</details>
<details>
<summary>Plot cumulative count of different reactions on a single plot</summary>

 ![](images/cumulative_rxns.png)
</details>

[↥ back to top](#table-of-contents)


## Observations


1. There is a spike in friends made in March (Election season) and July (new juniors, much higher spike).

2. I tend to message less during exams (Feb, Apr, Sep, Nov).

3. Highest number of messages sent at 9 and 11 pm, confirming with calls from home come at 10pm. Almost no messages shared between 3am-7am.

4. I used to send more friend request as compared to friend request received.
 	 
5. I tend to receive more friend request in the month of july,august(new juniors)

[↥ back to top](#table-of-contents)

## Why

I always wanted to know how many friends I make every month. It would have been infeasible to make a webapp out of this because so many API calls would be so _slow_, and whosoever wants to work with Facebook's Graph API?

Plus it was raining and I couldn't go to MS's Hall Day till after the rain stopped.

Have a feature request? See an interesting avenue not utilised yet with facebook's archive? Let me know by making a new issue.

[↥ back to top](#table-of-contents)

## License

The MIT License (MIT) 2018 - [Kaustubh Hiware](https://github.com/kaustubhhiware). Please have a look at the [LICENSE](LICENSE) for more details.
