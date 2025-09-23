export const checkURL = (url: string): boolean => {

    if (!url) return false;

    const urlPattern = /^(https?:\/\/)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(\S*)?$/;
    return urlPattern.test(url);
}

export const checkHTTP = (url: string): string => {

    if (!/^https?:\/\//.test(url)) {
        return 'https://' + url;
    }

    return url
}