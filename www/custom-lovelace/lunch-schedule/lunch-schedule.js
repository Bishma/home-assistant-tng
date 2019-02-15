class LunchSchedule extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }
    setConfig(config) {
        /**
         * An entity to use to trigger a refresh for static dashboards.
         * @TODO Add a timer so the refresh is just set at 4h 
         */
        if (!config.entity) {
            throw new Error('Please define an entity');
        }

        /**
         * Blank the old card if there is one
         */
        const root = this.shadowRoot;
        if (root.lastChild) {
            root.removeChild(root.lastChild);
        }


        /**
         * Ensure the config is an object
         */
        const userConfig = Object.assign({}, config);

        /**
         * Define the card as an object
         */
        const card = document.createElement('ha-card');
        if (userConfig.title) {
            card.header = userConfig.title;
        }

        const content = document.createElement('div');
        content.id = "primary-content"
        const style = document.createElement('style');
        style.textContent = `
            ha-card {
            }
            #primary-content {
                padding: 0 10px 12px 26px;
            }
            #primary-content li {
                list-style-type: none;
                font-family: Roboto, sans-serif;
                -moz-osx-font-smoothing: grayscale;
                -webkit-font-smoothing: antialiased;
                font-weight: 400;
                padding: 12px;
            }
        `;
        card.appendChild(content);
        card.appendChild(style);
        root.appendChild(card);
        this._config = userConfig;
    }
  
    set hass(hass) {
        const userConfig = this._config;
        const root = this.shadowRoot;

        const nextThree = hass.states[userConfig.entity].attributes["nextThree"];
  
        if (nextThree !== this._nextThree) {
            let cardContent = "";
            for (let i = 0; i < nextThree.length; i++) {
                cardContent += `<li>${nextThree[i]}</li>`;
            }

            root.getElementById("primary-content").innerHTML = `<ul>${cardContent}</ul>`;

            this._nextThree = nextThree
        }
        root.lastChild.hass = hass;
    }

    
  
    getCardSize() {
        return 2;
    }
}

customElements.define('lunch-schedule', LunchSchedule);