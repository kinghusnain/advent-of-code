import org.junit.jupiter.api.Test

class Day24Tests {
    val input = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

    @Test
    fun pt1() {
        val tileGrid = HexGrid()
        tileGrid.flipTiles(input.split("\n"))
        assert(tileGrid.blackTileCount() == 10)
    }

    @Test
    fun pt2() {
        val tileGrid = HexGrid()
        tileGrid.flipTiles(input.split("\n"))
        tileGrid.expand()
        assert(tileGrid.blackTileCount() == 10)

        tileGrid.dailyFlips()
        assert(tileGrid.blackTileCount() == 15)
        tileGrid.dailyFlips()
        assert(tileGrid.blackTileCount() == 12)
        tileGrid.dailyFlips()
        assert(tileGrid.blackTileCount() == 25)
        for (n in 4..100) {
            tileGrid.dailyFlips()
        }
        assert(tileGrid.blackTileCount() == 2208)
    }
}