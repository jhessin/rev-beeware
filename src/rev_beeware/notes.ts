export async function remoteHasNewer(localDate: Date): Promise<[boolean, Date]> {
  try {
    let dateJson: iDateJson = await fetch(URL)
      .then(res => res.json())
      .catch(err => {
        console.error(`Error parsing date: ${err}`);
      });
    const remoteDate = new Date(dateJson.REV_Timestamp[0].timestamp);
    return [remoteDate.getTime() > localDate.getTime(), remoteDate];
  } catch (error) {
    console.error(`Error reading remote date: ${error}`);
  }
}

  private static async fetch(): Promise<Bible> {
    console.log('Fetching bible...');
    const bible: iBibleJson = await fetch(BIBLE_URL).then(res => res.json());
    console.log('Fetching commentary...');
    const commentary: iCommentaryJson = await fetch(COMMENTARY_URL).then(res => res.json());
    console.log('Fetching appendices...');
    const appendicesJson: iAppendicesJson = await fetch(APPENDICES_URL).then(res => res.json());
    console.log('All data fetched!');
    const verses = bible.REV_Bible.map(v =>
      Verse.fromOldVerse(v, commentary.REV_Commentary.filter(c => c.book === v.book && c.chapter === v.chapter.toString() && c.verse === v.verse.toString())[0]?.commentary || ''),
    );
    const [_, remoteDate] = await remoteHasNewer(new Date());
    const updated = remoteDate;
    let data = new Bible(verses, appendicesJson.REV_Appendices, updated);
    data.save();
    return data;
  }

export interface importVerse {
  book: string;
  chapter: number;
  verse: number;
  heading: string;
  microheading: number;
  paragraph: number;
  style: Style;
  footnotes: string;
  versetext: string;
}

export interface iBibleJson {
  // eslint-disable-next-line camelcase
  REV_Bible: importVerse[];
  updated?: Date;
}

export interface iAppendices {
  title: string;
  appendix: string;
}

export interface iAppendicesJson {
  REV_Appendices: iAppendices[];
  updated?: Date;
}

export interface iCommentary {
  book: string;
  chapter: number;
  verse: number;
  commentary: string;
}

export interface iStringCommentary {
  book: string;
  chapter: string;
  verse: string;
  commentary: string;
}

export interface iCommentaryJson {
  REV_Commentary: iStringCommentary[];
  updated?: Date;
}
