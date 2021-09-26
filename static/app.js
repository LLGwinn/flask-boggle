class BoggleGame {

    constructor(boardId, seconds=60) {
        this.seconds = seconds; // game length
        this.showTimer();

        this.score = 0;
        this.words = new Set();
        this.board = $("#" + boardId);

        // every 1000 msec, "tick"
        this.timer = setInterval(this.tick.bind(this), 1000);

        $('.add_word', this.board).on('submit', this.handleGuess.bind(this));
        
    }

    /* show word in list */
    showWord(word) {
        $('.words', this.board).append($('<li>', { text: word }));
    }

    /* show score in html */
    showScore() {
        $('.score', this.board).text(this.score);
    }

    /* show result message */
    showMessage(msg, cls) {
        $('.msg', this.board).text(msg).removeClass().addClass(`msg ${cls}`);
     }

    async handleGuess(evt) {
        evt.preventDefault();
        const $word = $('.word', this.board);
        let word = $word.val();

        // word is already in the list
        if (this.words.has(word)) {
            this.showMessage(`Already found ${word}`, 'err');
            return;
        }

        // check for valid word
        const response = await axios.get('/evaluate', {params: {word: word}});

        if (response.data.result === 'not-word') {
            this.showMessage(`${word} is not in the dictionary`, 'err');
        } else if (response.data.result === 'not-on-board') {
            this.showMessage(`${word} is not a valid word on the board`, 'err');
        } else {
            this.showWord(word);
            this.score += word.length;
            this.showScore();
            this.words.add(word);
            this.showMessage(`Added: ${word}`, 'ok');
        }

        $word.val("").focus();
    }

    /* Update timer in DOM */
    showTimer() {
        $('.timer', this.board).text(this.seconds);
    }

    /* Tick: handle a second passing in game */
    async tick() {
        this.seconds -= 1;
        this.showTimer();

        if (this.seconds === 0) {
            clearInterval(this.timer);
            await this.scoreGame();
        }
    }

    /* end of game: score and update message. */
    async scoreGame() {
        $('.add_word', this.board).hide();
        const response = await axios.post('/post_score', { score: this.score });
        if (response.data.brokeRecord) {
            this.showMessage(`New record: ${this.score}`, 'ok');
        } else {
        this.showMessage(`Final score: ${this.score}`, 'ok');
        }
    }
}

