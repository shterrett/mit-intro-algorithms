import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self):
      best_path = {}

      def pixel(c, r):
        return (c, r)

      def row(point):
        return point[1]

      def column(point):
        return point[0]

      def point(predecessor):
        return predecessor[0]

      def energy(predecessor):
        return predecessor[1]

      def total_energy(point):
        return energy(best_path[point])

      def predecessors(c, r):
        def out_of_bounds(point):
          column_out_of_bounds = column(point) < 0 or column(point) > (self.width - 1)
          row_out_of_bounds = row(point) < 0 or row(point) > (self.height - 1)
          return  column_out_of_bounds or row_out_of_bounds

        candidates = [pixel(c - 1, r - 1),
                      pixel(c, r - 1),
                      pixel(c + 1, r - 1)]
        return [point for point in candidates if not out_of_bounds(point)]

      for r in xrange(0,self.height):
        for c in xrange(0, self.width):
          preds = predecessors(c, r)
          predecessor = None
          if preds:
            predecessor = min(preds, key=total_energy)
          if predecessor:
            best_path[pixel(c, r)] = (predecessor, total_energy(predecessor) + self.energy(c, r))
          else:
            best_path[pixel(c, r)] = (None, self.energy(c, r))

      path_end = pixel(0, self.height - 1)
      for c in xrange(1, self.width):
        guess = pixel(c, self.height - 1)
        if total_energy(guess) < total_energy(path_end):
          path_end = guess

      path = []
      while path_end:
        path.append(path_end)
        path_end = point(best_path[path_end])

      path.reverse()
      return path

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
