import { AcGameObject } from "./AcGameObject";

export class GameUtils extends AcGameObject {
    constructor(store) {
        super();
        this.store = store;

        this.matchTime = 0;

        this.verifyCodeTime = 300;
    }

    initMatchTime() {
        this.matchTime = 0;
    }

    initVerifyCodeTime() {
        this.verifyCodeTime = 300 * 1000;
    }

    update() {
        if(this.store.state.utils.isMatch) {
            this.matchTime += this.timedelta;
            if(parseInt(this.matchTime / 1000) !== this.store.state.utils.matchTime) {
                this.store.commit("updateMatchTime", parseInt(this.matchTime / 1000));
            }
        }
        if(this.store.state.utils.showVerifyCode) {
            this.verifyCodeTime -= this.timedelta;
            if(parseInt(this.verifyCodeTime / 1000) !== this.store.state.utils.verifyCodeTime) {
                this.store.commit("updateVerifyCodeTime", parseInt(this.verifyCodeTime / 1000));
                if(this.verifyCodeTime / 1000 <= 0) {
                    this.store.commit("updateShowVerifyCode", false);
                }
            }
        }
    }
}