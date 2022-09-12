import { AcGameObject } from "./AcGameObject";

export class GameUtils extends AcGameObject {
    constructor(store) {
        super();
        this.store = store;

        this.matchTime = 0;
    }

    initMatchTime() {
        this.matchTime = 0;
    }

    update() {
        if(this.store.state.utils.isMatch) {
            this.matchTime += this.timedelta;
            if(parseInt(this.matchTime / 1000) != this.store.state.utils.matchTime) {
                this.store.commit("updateMatchTime", parseInt(this.matchTime / 1000));
            }
        }
    }
}