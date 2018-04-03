# facebook-archive
Just some fun you can have with facebook's archive data.

In light of the recent facebook's data breach, Mark Zuckerberg made all the data available for each user via Facebook. You're going to need to download it, we'll get to it shortly. There are some things that would take a lot of time (too costly API calls) online, but can be easily done on archived data.

## Getting the data

1. Head on to [Facebook > Settings > General Settings](https://www.facebook.com/settings).
2. Click on download archive. It might take some time to prepare the archive, this might take upto 10-15 minutes. NOTE: The download might be in order of 100s MBs. (Mine was 634MB).
 ![](images/archive-download.png)

## Features

### Your friends

* Plot the friends you make every day (blue), and the friends so far (orange).

 ![](images/friends-cumulative.png)

* Plot exclusively the friends you make each day.

 ![](images/friends-each.png)

### Messages

The following is available for either a specific chat (person / group) or for all messages.

* Plot all messages so far, with new messages each hour.

 ![](images/msgs-cumulative.png)

* Plot only new messages each hour.

 ![](images/msgs-each.png)

* Plot messages as a function of hour (0-24)

 ![](images/msgs-hour.png)

* Plot messages as a function of month.

 ![](images/msgs-month.png)

## Usage

### Friends

```
> python plot_friends.py
Enter facebook archive extracted location: "location of extracted, downloaded zip: like facebook-kaustubhhiware"
```

### Messages

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

## License

The MIT License (MIT) 2018 - [Kaustubh Hiware](https://github.com/kaustubhhiware). Please have a look at the [LICENSE](LICENSE) for more details.