##
## NOTE: This is not to scale. Just serves as a reference.
##
        ##  ##
        ## gutter
        ##  ##
        ##############################################################################  ### row 0
        ##  ##                                                                      ##
        ##  ##                                                                      ##
        ##  ##                                                                      ##
        ##  ##                                                                      ##
        ##  ##                                    main                              ##
        ##  ##                                                                      ##
        ##  ##                                                                      ##
        ##  ##                                                                      ##
        ##  ##                                                                      ##
        ##  ##                                                                      ##
        ##  ##                                                                      ##
        ##  ##                                                                      ##
        ##  ##                                                                      ##
        ##  ##                                                                      ##
        ##  ##                                                                      ##
        ##############################################################################  ### row 1
        ##                   ##                          ##                         ##
        ##    coroutines     ##          context         ##       stack             ##
        ##                   ##          watch           ##       breakpoints       ##
        ##                   ##          evaluate        ##                         ##
        ##                   ##                          ##                         ##
        ##                   ##                          ##                         ##
        ##############################################################################  ### row 2

        #    #                #                             #                        #
        #    #                #                             #                        #

# col   0    1                2                             3                        4


debug_layout = {
    "cols": [
        0.0, 0.05,             0.15,                           0.6,                     1.0
    ],
    "rows": [
        0.0,
        0.7,
        1.0
    ],
    "cells": [

        #[
        #   x1, y1,
        #   x2, y2
        #]

        # group 0: gutter
        [
            0, 0,
             1, 1
        ],

        # group 1: main text area
        [
            1, 0,
            4, 1
        ],

        # group 2: coroutines
        [
            0, 1,
            2, 2
        ],

        # group 3: context, watch, evaluate
        [
            2, 1,
            3, 2
        ],

        # group 4: stack, breakpoints
        [
            3, 1,
            4, 2
        ]
    ]
},

debug_layout_view_data = {
    "gutter": {
        "index": 0,
        "group": 0,
    },

    "coroutines": {
        "group": 2,
        "index": 0,
    },

    "context": {
        "group": 3,
        "index": 0,
    },
    "watch": {
        "group": 3,
        "index": 1,
    },
    "evaluate": {
        "group": 3,
        "index": 3,
    },

    "stack": {
        "group": 4,
        "index": 0,
    },
    "breakpoint": {
        "group": 4,
        "index": 1,
    },
}

