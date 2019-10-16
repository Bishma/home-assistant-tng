class WaqiMeter extends HTMLElement {
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
                .wrapper {
                    flex: 3;
                    height: 100%;
                    position: relative;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    overflow: hidden;
                    padding-bottom: 16px;
                }
                .wrapper img {
                    display: block;
                    display: inline-block;
                    max-width: 100%;
                    max-height: 100%;
                }
                .label {
                    position: absolute;
                    bottom: 24%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    font-family: var(--ha-card-header-font-family, inherit);
                    font-size: var(--ha-card-header-font-size, 24px);
                    letter-spacing: -0.012em;
                    line-height: 26px;
                    letter-spacing: -0.012em;
                }
                .value {
                    font-size: var(--ha-card-header-font-size, 24px);
                    font-weight: bold;
                }
                .units {
                    font-size: var(--ha-card-header-font-size, 16px);
                }
            `;
            card.appendChild(this.content);
            card.appendChild(style);
            this.appendChild(card);
        }

        const state = hass.states[this.config.entity];
        const unit = hass.states[this.config.entity].attributes.hasOwnProperty('unit_of_measurement') ? hass.states[this.config.entity].attributes['unit_of_measurement'] : "";
        let image = "";

        if (!isNaN(state.state)) {
            if (state.state <= 50) {
                image = "/local/air-quality/good.jpg";
            } else if (state.state <= 100) {
                image = "/local/air-quality/moderate.jpg";
            } else if (state.state <= 150) {
                image = "/local/air-quality/unhealthy-1.jpg";
            } else if (state.state <= 200) {
                image = "/local/air-quality/unhealthy-2.jpg";
            } else if (state.state <= 300) {
                image = "/local/air-quality/unhealthy-3.jpg";
            } else {
                image = "/local/air-quality/hazardous.jpg";
            }
        } else {
            image = "/local/air-quality/unknown.jpg"
        }

        let cardContent = `
            <div class="wrapper">
                <img src="${image}" />
                <div class="label">
                    <span class="value">${state.state}</span>
                    <span class="units">${unit}</span>
                </div>
            </div>
        `;

        this.content.innerHTML = cardContent;
    }

    determineImage() {
        
    }
    
    setConfig(config) {
        /**
         * The entity is required
         */
        if (!config.entity) {
            throw new Error('Please define an entity');
        }

        /**
         * Ensure the config is an object
         */
        config = Object.assign({}, config);
        this.config = config;
    }
    
    // The height of your card. Home Assistant uses this to automatically
    // distribute all cards over the available columns.
    getCardSize() {
        return 2;
    }
}

customElements.define('waqi-meter-card', WaqiMeter);