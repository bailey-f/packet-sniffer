
Refer to https://docs.google.com/document/d/1LXiltV4p79YEyUGhFiv5oBQvBsQUn4C2TEcohT2Q5Bs/edit?usp=sharing
```
                    +--------------+
                    |user interface|
                    +-------+------+
                            |
       +----------------------------------------------------------+
       |                    |                                     |
       | +---------+ +------+-------+  +-----------------------+  |
       | |         | |     GUI      |  |                       |  |
       | |         | +------+-------+  |    enhanced packet    |  |
       | | capture |        |          |       analyser        |  |
       | |         | +------+-------+  |                       |  |
```    | |         +-+[core / main] +--+                       |  |
```    | +----+----+ +--------------+  +-----------------------+  |
       |      |                                                   |
       +----------------------------------------------------------+
              |
        +-----+--------------------+
        |                          |
        |filtered data from network|
        |                          |
        +--------------------------+
```

  [core / main]: https://github.com/bailey-f/packet-sniffer/tree/homedev/Code/networksniffer/Core