class ListItem extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }
    setConfig(config) {
        /**
         * The entity is required
         */
        if (!config.entity) {
            throw new Error('Please define an entity');
        }

        /**
         * The attribute is required
         */
        if (!config.attribute) {
            throw new Error('Please define an attribute of the defined entity');
        }

        const root = this.shadowRoot;

        /**
         * Ensure the config is an object
         */
        const userConfig = Object.assign({}, config);

        /**
         * The definable max list length needs to be an integer
         * If anything is amiss default to 4
         */
        if (!userConfig.max_length || !Number.isInteger(userConfig.max_length)) {
            userConfig.max_length = 4;
        }

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
            .header { var(--primary-text-color); }
            .lc-wrapper {
				padding: 5px 5px 5px 20px;
				margin-bottom: 5px;
			}
			.lc-wrapper:last-child {
				padding-bottom: 18px;
			}
			.lc-wrapper .ha-icon {
				display: inline-block;
				height: 20px;
				width: 20px;
				margin-left: 5px;
				margin-right: 17px;
				color: var(--paper-item-icon-color);
			}
			.lc-item {
				display: inline-block;
				padding-left: 10px;
				padding-top: 2px;
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

        const listData = hass.states[userConfig.entity].attributes[userConfig.attribute];
        // if the list isn't a list say so
        if (!Array.isArray(listData)) {
            listData = [
                `The attribute '${userConfig.attribute}'`,
                ` of entity '${userConfig.entity}'`,
                ` is not a list.`
            ];
        }

        let iconAttr = '';
        if (userConfig.icon) {
            iconAttr = `icon='${userConfig.icon}'`
        }

        // the number of items to display is the small of userConfig.max_length or listData.length
        const listLength = userConfig.max_length < listData.length ? userConfig.max_length : listData.length;
  
        if (listData !== this._listData) {
            let cardContent = "";
            for (let i = 0; i < listLength; i++) {
                cardContent += `
                    <div class='lc-wrapper'>
                        <ha-icon class='ha-icon entity' ${iconAttr}></ha-icon>
                        <div class='lc-item'>${listData[i]}</div>
                    </div>`;
            }

            root.getElementById("primary-content").innerHTML = cardContent;

            this._listData = listData
        }
        root.lastChild.hass = hass;
    }

    getCardSize() {
        if (Number.isInteger(this._config.max_length)) {
            const cSize = 1 + Math.round(this._config.max_length / 4);
        } else {
            const cSize = 1;
        }
        return cSize;
    }
}

customElements.define('list-item-card', ListItem);