
// export let runValue;
// export let precValue;
// export let stockValue;
// export let startDate;
// export let endDate;
// export let chartSelected;
// export let chartContent;
// export let riskTarget;

// export const appState = {
//     state: 0,
//     codes: 'AAPL, MSFT, AMZN',
//     runs: 1000,
//     precision: 1,
//     start: '2024-01-01',
//     end: '2024-05-01',
//     chart: '',
//     charts: '',
//     html: '',
//     target: ''
// };

export async function postFetch(data) {
    try {
        const response = await fetch('/post/state', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        let resp = await response.json();
        console.log("post_resp", resp);
        return resp;
    } catch (e) {
        console.error("error", e);
    }
}


export async function getFetch() {
    try {
        const response = await fetch('/get/state');
        let resp = await response.json();
        console.log("get_resp", resp);
        // console.log(resp);
        return resp;
    } catch (e) {
        console.error("error", e);
    }
}


