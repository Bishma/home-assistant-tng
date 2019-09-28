class ListItem extends HTMLElement {
    set hass(hass) {
        if (!this.content) {
            const card = document.createElement('ha-card');
            if (this.config.title) {
                // @TODO: support entity friendly_name if available and config.title is not
                card.header = this.config.title;
            }
            this.content = document.createElement('div');
            let style = document.createElement('style');
            style.textContent = `
                ha-card .header { var(--primary-text-color); }
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
            card.appendChild(this.content);
            card.appendChild(style);
            this.appendChild(card);
        }

        let listData = hass.states[this.config.entity].attributes[this.config.attribute];
        // if the list isn't a list say so
        if (!Array.isArray(listData)) {
            listData = [
                `The attribute '${this.config.attribute}'`,
                ` of entity '${this.config.entity}'`,
                ` is not a list.`
            ];
        }

        // the number of items to display is the small of this.config.max_length or listData.length
        const listLength = this.config.max_length < listData.length ? this.config.max_length : listData.length;

        let cardContent = "";
        for (let i = 0; i < listLength; i++) {
            cardContent += `
                <div class='lc-wrapper'>
                    <ha-icon class='ha-icon entity' ${this.config['list_icon']}></ha-icon>
                    <div class='lc-item'>${listData[i]}</div>
                </div>`;
        }

        this.content.innerHTML = cardContent;
    }
    
    setConfig(config) {
        /**
         * The entity is required
         */
        if (!config.entity) {
            throw new Error('Please define an entity');
        }

        /**
         * The attribute from the entity above is also required
         */
        if (!config.attribute) {
            throw new Error('Please define an attribute of the defined entity');
        }

        /**
         * Ensure the config is an object
         */
        config = Object.assign({}, config);

        /**
         * The definable max list length needs to be an integer
         * If anything is amiss default to 4
         */
        if (!config.max_length || !Number.isInteger(config.max_length)) {
            config.max_length = 4;
        }

        /**
         * List item icons are optional
         * @TODO: use the entity's icon if available and config.icon is not
         */
        config['list_icon'] = '';
        if (config.icon) {
            config['list_icon'] = `icon='${config.icon}'`
            delete config.icon;
        }

        this.config = config;
    }
    
    // The height of your card. Home Assistant uses this to automatically
    // distribute all cards over the available columns.
    getCardSize() {
        return 1;
    }
}

customElements.define('list-item-card', ListItem);